---
title: "2005-08-02자 I2P 상태 노트"
date: 2005-08-02
author: "jr"
description: "0.6 릴리스 상태, PeerTest 시스템, SSU introductions(소개 절차), I2PTunnel 웹 인터페이스 수정, 그리고 I2P 상의 mnet을 다루는 뒤늦은 업데이트"
categories: ["status"]
---

안녕하세요 여러분, 오늘은 노트가 늦었습니다,

* Index:

1) 0.6 진행 상황 2) PeerTest 3) SSU 소개 4) I2PTunnel 웹 인터페이스 5) i2p 상의 mnet 6) ???

* 1) 0.6 status

여러분도 보셨듯이 며칠 전 0.6 릴리스를 배포했으며, 전반적으로는 꽤 순조롭게 진행되고 있습니다. 0.5.* 이후의 전송 계층 개선으로 인해 netDb 구현의 몇 가지 문제가 드러났지만, 그 대부분에 대한 수정은 현재 0.6-1 빌드로 테스트 중이며 조만간 0.6.0.1로 배포될 예정입니다. 또한 다양한 NAT 및 방화벽 설정에서의 문제와 일부 사용자들의 MTU 문제에도 부딪혔는데, 이는 테스터 수가 적었던 소규모 테스트 네트워크에서는 나타나지 않았던 문제들입니다. 가장 심각한 사례들에는 우회책을 추가했지만, 머지않아 장기적인 해결책도 도입할 예정입니다 - peer tests(피어 테스트).

* 2) PeerTest

With 0.6.1, we're going to deploy a new system to collaboratively test and configure the public IPs and ports. This is integrated within the core SSU protocol and will be backwards compatible. Essentially what it does is lets Alice ask Bob what her public IP and port number is, and then in turn have Bob get Charlie to confirm her proper configuration, or to find out what the limitation preventing properation is. The technique is nothing new on the net, but is a new addition to the i2p codebase and should remove most common configuration error.

* 3) SSU introductions

SSU 프로토콜 명세에 설명된 대로, 방화벽과 NAT 뒤에 있는 사용자들이 비요청 UDP 메시지를 수신할 수 없더라도 네트워크에 완전히 참여할 수 있게 하는 기능이 제공될 예정이다. 이 기능이 모든 가능한 상황에서 작동하는 것은 아니지만, 대부분을 해결할 것이다. SSU 명세에 설명된 메시지들과 PeerTest(피어 테스트)에 필요한 메시지들 사이에는 유사성이 있으므로, 그 메시지들이 명세에 반영될 때 소개 메시지(introductions)를 PeerTest 메시지에 끼워 보낼 수 있을 것이다. 어쨌든 이러한 소개 메시지는 0.6.2에서 도입되며, 이 역시 하위 호환성을 유지한다.

* 4) I2PTunnel web interface

일부 사람들이 I2PTunnel 웹 인터페이스에서 여러 가지 이상 현상을 발견해 보고했으며, smeghead가 필요한 수정 사항을 정리하기 시작했습니다 - 아마도 그는 해당 업데이트에 대해 더 자세히 설명하고, 이에 대한 ETA(예상 완료 시점)도 알려줄 수 있을까요?

* 5) mnet over i2p

논의가 진행되는 동안에는 채널에 없었지만, 로그를 읽어보니 icepick이 I2P 위에서 mnet이 동작하도록 만들기 위한 개발 작업을 해오고 있으며, 이를 통해 mnet 분산 데이터 저장소가 익명으로 운영되면서도 복원력 있는 콘텐츠 게시를 제공할 수 있도록 하려는 것 같습니다. 이 부분의 진행 상황을 제가 자세히 알지는 못하지만, SAM과 Twisted를 통해 I2P와의 연동에서 icepick이 꽤 좋은 진전을 이루고 있는 듯합니다. 아마 icepick이 더 자세히 알려줄 수 있겠지요?

* 6) ???

음, 위에 쓴 것보다 진행 중인 일이 훨씬 더 많지만, 벌써 늦었으니 여기까지만 쓰고 이 메시지를 먼저 보낼게요. 오늘 저녁에 잠깐 온라인에 접속할 수 있을 것 같아서, 혹시 계시면 오후 9시 30분쯤(이걸 받는 대로 ;) 평소의 IRC 서버 {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net}의 #i2p에서 회의를 하면 좋겠습니다.

기다려 주시고 일이 진전되도록 도와주셔서 감사합니다!

=jr
