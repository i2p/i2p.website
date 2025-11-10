---
title: "2004-07-20자 I2P 상태 노트"
date: 2004-07-20
author: "jr"
description: "0.3.2.3 릴리스, 용량 변경, 웹사이트 업데이트, 보안 고려 사항을 다루는 주간 상태 업데이트"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, 그리고 로드맵**

지난주 0.3.2.3 릴리스 이후, 여러분 모두가 업그레이드를 아주 훌륭하게 진행해 주셨습니다 — 이제 업그레이드하지 않은 경우는 두 개만 남았습니다(하나는 0.3.2.2, 또 하나는 한참 이전인 0.3.1.4 :)). 지난 며칠 동안 네트워크가 평소보다 더 안정적으로 동작했고, 사람들이 irc.duck.i2p에 여러 시간씩 머물러 있으며, eepsites(I2P Sites)에서 큰 파일 다운로드도 성공하고 있고, 전반적인 eepsite(I2P Site) 접근성도 꽤 좋습니다. 상황이 잘 돌아가고 있고 여러분이 방심하지 않도록, 몇 가지 근본적인 개념을 바꾸기로 했고 하루이틀 내에 0.3.3 릴리스로 배포할 예정입니다.

몇몇 분들이 우리가 올려둔 일정대로 맞출 수 있을지에 대해 의견을 주셔서, 제 팜파일럿에 있는 로드맵을 반영하도록 웹사이트를 업데이트해야겠다고 판단했고, 그래서 그렇게 했습니다 [1]. 날짜들은 지연되었고 일부 항목들이 이동되었지만, 계획 자체는 지난달에 논의했던 것과 변함없습니다 [2].

0.4는 언급된 네 가지 릴리스 기준(기능성, 보안성, 익명성, 확장성)을 충족하겠지만, 0.4.2 이전에는 NAT와 방화벽 뒤에 있는 소수만이 참여할 수 있으며, 0.4.3 이전에는 다른 router에 대한 대량의 TCP 연결을 유지하는 데 따른 오버헤드 때문에 네트워크의 크기에 실질적인 상한이 존재하게 된다.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

지난 일주일 정도 동안, #i2p에 있는 사람들은 우리의 신뢰성 순위가 완전히 자의적이라는 점(그리고 그것이 최근 몇 차례 릴리스에서 야기한 골칫거리)에 대해 제가 가끔 하소연하는 것을 들었을 겁니다. 그래서 우리는 신뢰성이라는 개념을 완전히 없애고, 그 대신 처리 능력(capacity) 측정 - "피어가 우리를 위해 얼마나 많은 일을 해줄 수 있는가?" - 으로 대체했습니다. 이는 피어 선택과 피어 프로파일링 코드 전반에 (그리고 당연히 router 콘솔에도) 파급 효과를 가져왔지만, 그 외에는 크게 바뀐 것은 없습니다.

이 변경 사항에 대한 추가 정보는 개정된 피어 선택 페이지 [3]에서 확인할 수 있으며, 0.3.3이 릴리스되면 여러분 모두가 그 영향을 직접 확인하실 수 있을 것입니다(저는 지난 며칠 동안 이리저리 만져 보며 설정을 조금씩 조정하는 등 테스트해 왔습니다).

[3] http://www.i2p.net/redesign/how_peerselection

**3) 웹사이트 업데이트**

지난 일주일 동안 우리는 웹사이트 리디자인 [4] - 내비게이션을 단순화하고, 몇몇 핵심 페이지를 정리하고, 기존 콘텐츠를 이관하고, 새 항목 몇 가지 [5]를 작성했습니다. 사이트를 라이브로 전환할 준비가 거의 되었지만, 아직 해야 할 일이 몇 가지 남아 있습니다.

오늘 일찍 duck이 사이트를 점검하여 누락된 페이지 목록을 작성했고, 오늘 오후의 업데이트 이후에도 우리가 직접 해결하든 자원봉사자들이 나서주길 바라는 몇 가지 미해결 문제가 남아 있습니다:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

그 외에는 사이트를 라이브로 전환할 준비가 거의 다 된 것 같습니다. 그와 관련해 제안이나 우려 사항이 있으신가요?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) 공격과 방어**

Connelly는 네트워크의 보안과 익명성의 허점을 찾아내기 위해 몇 가지 새로운 접근법을 고안해 왔고, 그 과정에서 우리가 개선할 수 있는 방법들도 발견했습니다. 그가 설명한 기법의 일부 측면은 I2P와 꼭 들어맞지는 않지만, 여러분이라면 그것들을 확장해 네트워크를 더 깊이 공격할 수 있는 방법을 찾아낼 수도 있지 않을까요? 자, 한번 시도해 보세요 :)

**5) ???**

오늘 밤 회의 전에 제가 기억나는 건 대략 이 정도입니다 - 제가 놓친 것이 있으면 편하게 말씀해 주세요. 아무튼, 몇 분 뒤에 #i2p에서 봬요.

=jr
