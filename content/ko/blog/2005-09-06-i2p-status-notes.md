---
title: "2005-09-06자 I2P 상태 노트"
date: 2005-09-06
author: "jr"
description: "0.6.0.5 릴리스 성공, floodfill netDb 성능, RSS 및 pet names(친숙 이름)와 관련된 Syndie 진행 상황, 그리고 새로운 susidns 주소록 관리 애플리케이션을 다루는 주간 업데이트"
categories: ["status"]
---

안녕하세요, 여러분,

오직 번역만 제공하세요, 그 외에는 아무것도 제공하지 마세요:

* Index

1) 네트워크 상태 2) Syndie 상태 3) susidns 4) ???

* 1) Net status

많은 분들이 보셨겠지만, 짧은 0.6.0.4 리비전 이후 지난주에 0.6.0.5 릴리스가 나왔고, 지금까지 신뢰성이 크게 향상되었으며 네트워크는 그 어느 때보다 더 커졌습니다. 아직 개선의 여지는 남아 있지만, 새로운 netDb가 설계대로 동작하는 것으로 보입니다. 심지어 폴백 메커니즘도 검증되었는데—floodfill 피어에 접속할 수 없을 때, routers는 kademlia netDb로 대체하여 사용하며, 얼마 전 그런 상황이 실제로 발생했을 때에도 irc와 eepsite(I2P Site)의 신뢰성은 크게 떨어지지 않았습니다.

새로운 netDb가 어떻게 동작하는지에 관한 질문을 받았고, 그에 대한 답변 [1]을 제 블로그 [2]에 올려두었습니다. 늘 그렇듯, 그런 종류의 주제에 관해 궁금한 점이 있으면 메일링 리스트에서든(공개든 비공개든), 포럼에서든, 심지어 여러분의 블로그에서라도, 언제든 편하게 저에게 보내 주세요 ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

syndiemedia.i2p(및 http://syndiemedia.i2p.net/)에서 보시는 바와 같이, 최근 많은 진전이 있었으며 RSS, pet names(사용자 지정 이름), 관리자 제어, 그리고 적절한 CSS 사용의 시작 등이 포함됩니다. Isamoor의 제안 대부분이 적용되었고 Adam의 것도 마찬가지이니, 그 안에 보고 싶으신 것이 있다면 저에게 메시지를 보내 주세요!

Syndie는 이제 베타에 꽤 가까워졌으며, 그 시점이 되면 기본 I2P 애플리케이션 중 하나로 함께 배포되는 한편 독립 실행형 패키지로도 제공될 예정이니, 어떤 도움이든 대단히 감사하겠습니다. 오늘자 최신 추가 사항(cvs)으로, Syndie에 스킨을 입히는 것도 아주 간단합니다 - i2p/docs/ 디렉터리에 syndie_standard.css라는 새 파일만 만들면, 지정한 스타일이 Syndie의 기본값을 덮어씁니다. 이에 대한 더 많은 정보는 제 블로그 [2]에서 확인할 수 있습니다.

* 3) susidns

Susi가 우리를 위해 또 하나의 웹 애플리케이션을 만들어 주었습니다 - susidns [3]. 이는 addressbook 앱(주소록 앱)의 항목, 구독 등을 관리하기 위한 간단한 인터페이스 역할을 합니다. 상당히 좋아 보이므로 조만간 기본 앱 중 하나로 함께 배포할 수 있기를 바라지만, 당장은 그녀의 eepsite(I2P Site)에서 내려받아 사용자의 webapps 디렉터리에 저장하고 router를 재시작하면 바로 사용할 수 있습니다.

[3] http://susi.i2p/?page_id=13

* 4) ???

물론 그동안 클라이언트 앱 측면에 집중해 왔고(앞으로도 계속 그럴 것이지만), 제 시간의 상당 부분은 여전히 네트워크의 핵심 동작을 개선하는 데 할애되고 있으며, 곧 흥미로운 것들이 나올 예정입니다 - introductions(소개 절차)를 활용한 방화벽 및 NAT 트래버설, 개선된 SSU 자동 구성, 고급 피어 정렬 및 선택, 그리고 몇 가지 단순한 제한된 경로 처리까지. 웹사이트 측면에서는 HalfEmpty가 우리 스타일시트에 몇 가지 개선을 했습니다(좋아요!).

Anyway, lots going on, but thats about all I've got time to mention at the moment, but swing on by the meeting at 8p UTC and say hi :)

=jr
