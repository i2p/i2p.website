---
title: "2005-08-16자 I2P 현황 노트"
date: 2005-08-16
author: "jr"
description: "PeerTest 상태, Irc2P 네트워크 전환, Feedspace GUI 진행 상황, 그리고 회의 시간을 GMT 기준 오후 8시로 변경하는 내용에 대한 간략한 업데이트"
categories: ["status"]
---

여러분 안녕하세요, 오늘은 간단히 메모만 드립니다.

* Index:

1) PeerTest 상태 2) Irc2P 3) Feedspace 4) 메타 5) ???

* 1) PeerTest status

앞서 언급했듯이, 곧 출시될 0.6.1 릴리스에는 router를 보다 세심하게 구성하고 도달 가능성을 확인(또는 필요한 조치를 지적)하기 위한 일련의 테스트가 포함될 것이다. 이미 두 번의 빌드 동안 CVS에 일부 코드가 있었지만, 필요한 만큼 매끄럽게 동작하기까지는 아직 다듬어야 할 부분이 남아 있다. 현재로서는, Charlie의 도달 가능성을 확인하기 위한 추가 패킷을 넣고 Charlie가 응답할 때까지 Bob이 Alice에게 보내는 응답을 지연시키는 방식으로, 문서화된 [1] 테스트 흐름에 약간의 수정을 가하고 있다. 이는 테스트할 준비가 된 Charlie가 확보될 때까지 Bob이 Alice에게 응답하지 않게 되므로 사람들이 보게 되는 불필요한 "ERR-Reject" 상태 값의 수를 줄여줄 것이다(그리고 Bob이 응답하지 않을 때, Alice는 상태로 "Unknown"을 보게 된다).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

어쨌든, 네, 그렇습니다 - 내일 0.6.0.2-3이 나올 예정이며, 철저히 테스트되면 정식 릴리스로 배포할 겁니다.

* 2) Irc2P

포럼 [2]에서 언급된 것처럼, IRC를 사용하는 I2P 사용자들은 새 IRC 네트워크로 전환하도록 설정을 업데이트해야 합니다. duck은 [redacted]로 인해 일시적으로 오프라인이 될 예정이며, 그 기간 동안 서버에 문제가 없기만을 바라기보다는, postman과 smeghead가 나서서 여러분이 사용할 새 IRC 네트워크를 구축했습니다. 또한 postman은 [3]에서 duck의 트래커와 i2p-bt 사이트도 미러링했으며, 새 IRC 네트워크에서 susi가 새로운 IdleRPG 인스턴스를 가동한다는 얘기를 본 것 같습니다(자세한 내용은 채널 목록을 확인하세요).

옛 i2pirc 네트워크를 맡아 주셨던 분들(duck, baffled, the metropipe crew, postman)과 새 irc2p 네트워크를 운영하시는 분들(postman, arcturus)께 감사드립니다! 흥미로운 서비스와 콘텐츠가 I2P를 사용할 가치 있게 만들며, 그런 것들을 만들어 내는 일은 여러분 모두에게 달려 있습니다!

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

그 얘기가 나와서 말인데, 며칠 전에 frosk의 블로그를 읽다가 Feedspace에도 진전이 좀 있다는 걸 봤어요—특히 깔끔한 작은 GUI(그래픽 사용자 인터페이스) 쪽으로요. 아직 테스트할 단계는 아닐지도 알지만, 때가 되면 frosk가 우리에게 코드를 공유해 줄 거라고 믿어요. 참고로, 준비 중인 또 다른 익명성을 고려한 웹 기반 블로깅 도구에 대한 소문도 들었는데, 준비가 되면 Feedspace와 연동할 수 있을 거라고 해요. 역시 그건 준비가 되면 더 많은 정보를 듣게 되겠죠.

* 4) meta

제가 워낙 욕심 많은 놈이라서, 회의 시간을 조금 앞당기고 싶어요 - GMT 기준 오후 9시 대신 오후 8시로 해보죠. 왜냐고요? 제 일정에 더 잘 맞거든요 ;) (가장 가까운 인터넷 카페들이 너무 늦게까지는 문을 열지 않아서요).

* 5) ???

일단 지금은 이 정도입니다 - 오늘 밤 회의를 위해 인터넷 카페 근처에 있으려고 하니, /new/ irc 서버 {irc.postman.i2p, irc.arcturus.i2p}에서 GMT 기준 *8*P에 #i2p로 편하게 들러 주세요. irc.freenode.net으로 연결되는 changate 봇을 띄울 수도 있습니다 - 누가 하나 돌려 보실래요?

안녕, =jr
