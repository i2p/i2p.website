---
title: "2006-08-01자 I2P 상태 노트"
date: 2006-08-01
author: "jr"
description: "높은 I2PSnark 전송률, NTCP 트랜스포트 안정성, 그리고 eepsite 도달성에 대한 설명을 갖춘 강력한 네트워크 성능"
categories: ["status"]
---

안녕하세요, 여러분. 오늘 밤 회의 전에 간단한 메모 몇 가지를 공유하려 합니다. 여러분이 제기하실 다양한 질문이나 이슈가 있을 것으로 생각하므로, 오늘은 평소보다 더 유연한 형식으로 진행하겠습니다. 다만 먼저 언급하고 싶은 사항이 몇 가지 있습니다.

* Network status

네트워크가 꽤 잘 동작하는 것으로 보입니다. 상당히 큰 I2PSnark 전송의 swarms(스웜)들이 완료되고, 개별 router에서도 상당한 전송 속도가 달성되고 있습니다 — 저는 650KBytes/sec와 17,000개의 참여하는 tunnels를 별다른 문제 없이 본 적이 있습니다. 스펙트럼의 하위권에 있는 저사양 router들도 문제없이 동작하며, 2 hop tunnels로 eepsites(I2P Sites)와 irc를 브라우징하면서 평균 1KByte/sec 미만만 사용합니다.

모든 사람에게 장밋빛이기만 한 것은 아니지만, 보다 일관되고 실제 사용에 적합한 성능을 제공할 수 있도록 router의 동작을 업데이트하는 작업을 진행하고 있습니다.

* NTCP

새 NTCP transport("new" tcp)는 초기의 시행착오를 정리한 이후 꽤 잘 작동하고 있습니다. 자주 묻는 질문에 답하자면, 장기적으로는 NTCP와 SSU가 모두 운용될 것이며 - TCP-only로 되돌아갈 계획은 없습니다.

* eepsite(I2P Site) reachability

여러분, eepsites(I2P Sites)는 운영자가 가동 중일 때만 접속할 수 있다는 점을 기억하세요 - 다운되어 있으면 거기에 접속할 방법은 없습니다 ;) 불행히도 지난 며칠 동안 orion.i2p에는 접속할 수 없었지만, 네트워크는 확실히 여전히 작동하고 있습니다 - 네트워크 조사가 필요하시다면 inproxy.tino.i2p 또는 eepsites(I2P Sites).i2p에 들러 보세요.

Anyway, there's lots more going on, but it'd be a bit premature to mention it here. Of course, if you have any questions or concerns, swing on by #i2p in a few minutes for our *cough* weekly development meeting.

우리가 앞으로 나아가도록 도와주셔서 감사합니다! =jr
