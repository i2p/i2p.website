---
title: "2005-11-08자 I2P 상태 노트"
date: 2005-11-08
author: "jr"
description: "0.6.1.4 안정성, 성능 최적화 로드맵, I2Phex 0.1.1.35 릴리스, I2P-Rufus BT 클라이언트 개발, I2PSnarkGUI 진행 상황, Syndie UI 개편을 다루는 주간 업데이트"
categories: ["status"]
---

안녕, 여러분. 또 화요일이네요

* Index

1) 네트워크 상태 / 단기 로드맵 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

0.6.1.4 still seems pretty solid, though there have been some bugfixes in CVS since then. I've also added some optimizations for SSU to transfer data more efficiently, which I hope will have a noticeable impact on the network once its rolled out widely. I'm holding off on 0.6.1.5 for the moment though, as there are a few other things I want to get into the next release. The current plan is to push it out this weekend, so keep an ear out for the latest news.

0.6.2 릴리스에는 더 강력한 적대자에 맞서기 위한 많은 훌륭한 개선 사항이 포함되겠지만, 성능에는 영향을 미치지 않을 것입니다. I2P의 핵심은 분명 익명성이지만, 처리량이 낮고 지연이 크면 사용자가 없을 것입니다. 따라서 0.6.2의 피어 정렬 전략과 새로운 tunnel 생성 기법을 구현하는 단계로 넘어가기 전에, 성능을 필요한 수준까지 끌어올리는 것이 제 계획입니다.

* 2) I2Phex

최근 I2Phex 쪽에서도 활동이 많았고, 새로운 0.1.1.35 릴리스가 나왔습니다 [1]. 또한 CVS에도 추가 변경 사항이 있었으며(고마워요, Legion!), 이번 주 후반에 0.1.1.36이 나와도 놀랍지 않겠습니다.

gwebcache 쪽에서도 상당한 진전이 있었습니다(see http://awup.i2p/), 하지만 제가 아는 한 I2P 지원 gwebcache를 사용하도록 I2Phex를 수정하는 작업을 시작한 사람은 아직 없습니다(관심 있으신가요? 알려 주세요!).

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

소문에 따르면 defnax와 Rawn이 Rufus BT 클라이언트를 손보면서 I2P-BT에서 I2P 관련 코드를 일부 병합하고 있다고 합니다. 현재 포팅 상태는 잘 모르지만, 몇 가지 좋은 기능이 들어갈 것 같다고 합니다. 전할 내용이 더 생기면 분명 추가 소식을 들을 수 있을 것입니다.

* 4) I2PSnarkGUI

또 다른 소문으로는 Markus가 새로운 C# GUI를 두고 이것저것 개발 작업을 하고 있다는 것이다... PlanetPeer에 올라온 스크린샷이 꽤 멋지다[2]. 여전히 플랫폼에 독립적인 웹 인터페이스 계획도 있지만, 이것도 꽤 좋아 보인다. GUI가 진척됨에 따라 Markus에게서 더 많은 소식을 듣게 될 것이다.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

또한 Syndie UI 개편 [3]과 관련한 논의도 진행 중이며, 조만간 그 부분에서 어느 정도 진전을 보게 될 것으로 기대합니다. dust는 Sucker 작업에도 매진하고 있으며, Syndie로 더 많은 RSS/Atom 피드를 가져올 수 있도록 지원을 개선하는 한편, SML 자체에 대한 몇 가지 개선도 추가하고 있습니다.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

늘 그렇듯이, 정말 많은 일들이 진행 중입니다. 잠시 후 주간 개발 회의를 위해 #i2p에 들러 주세요.

=jr
