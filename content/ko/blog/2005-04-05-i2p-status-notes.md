---
title: "2005-04-05자 I2P 상태 노트"
date: 2005-04-05
author: "jr"
description: "0.5.0.5 릴리스 이슈, 베이지안 피어 프로파일링 연구, 그리고 Q 애플리케이션 진행 상황을 다루는 주간 업데이트"
categories: ["status"]
---

안녕하세요 여러분, 주간 업데이트 시간입니다

* Index

1) 0.5.0.5 2) 베이지안 피어 프로파일링 3) Q 4) ???

* 1) 0.5.0.5

지난주 0.5.0.5 릴리스는 우여곡절이 있었습니다 - netDb에서의 일부 공격에 대응하기 위한 주요 변경 사항은 기대한 대로 동작하는 것으로 보이지만, netDb의 동작에서 오랫동안 간과되어 온 몇 가지 버그를 드러냈습니다. 이로 인해, 특히 eepsites(I2P Sites)에 상당한 신뢰성 문제가 발생했습니다. 그러나 이러한 버그들은 CVS에서 식별되어 해결되었으며, 그 수정 사항들은 몇 가지 다른 수정과 함께 다음 하루 이내에 0.5.0.6 릴리스로 배포될 예정입니다.

* 2) Bayesian peer profiling

bla has been doing some research into improving our peer profiling by exploiting simple bayesian filtering from the gathered stats [1]. It looks quite promising, though I'm not sure where it stands at the moment - perhaps we can get an update from bla during the meeting?

[1] http://forum.i2p.net/viewtopic.php?t=598     http://theland.i2p/nodemon.html

* 3) Q

aum의 Q 앱에는 핵심 기능은 물론, 몇몇 사람들이 다양한 xmlrpc 프런트엔드를 구축하면서 많은 진전이 이루어지고 있습니다. 소문에 따르면 이번 주말에 http://aum.i2p/q/ 에 설명된 여러 가지 멋진 기능이 담긴 또 다른 Q 빌드를 보게 될지도 모릅니다.

* 4) ???

음, 네, 시간대를 *또다시* 헷갈려서(사실 요일도 헷갈려서 몇 시간 전까지 월요일인 줄 알았어요) 아주 간단한 상태 메모만 남길게요. 어쨌든, 위에 언급되지 않은 일들이 많으니, 회의에 들러서 무슨 일이 있는지 확인해 보세요!

=jr
