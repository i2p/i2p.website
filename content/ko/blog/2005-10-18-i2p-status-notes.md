---
title: "2005-10-18자 I2P 상태 노트"
date: 2005-10-18
author: "jr"
description: "0.6.1.3 릴리스 성공, Freenet 협업 논의, tunnel 부트스트랩 공격 분석, I2Phex 업로드 버그 진행 상황, 그리고 대칭 NAT 현상금을 다루는 주간 업데이트"
categories: ["status"]
---

안녕하세요 여러분, 또 화요일이네요

* Index

1) 0.6.1.3 2) Freenet, I2P, 그리고 다크넷 (세상에) 3) Tunnel 부트스트랩 공격 4) I2Phex 5) Syndie/Sucker 6) ??? [500+ 대칭 NAT 현상금]

* 1) 0.6.1.3

지난 금요일에 새로운 0.6.1.3 릴리스를 배포했으며, 네트워크의 70%가 업그레이드된 가운데 보고는 매우 긍정적입니다. 새로운 SSU 개선 사항은 불필요한 재전송을 줄인 것으로 보이며, 더 높은 속도에서도 더 효율적인 처리량을 가능하게 했고, 제가 알기로 IRC proxy나 Syndie 개선과 관련한 큰 문제는 없었습니다.

주목할 만한 점 한 가지는 Eol이 rentacoder[1]에 대칭 NAT 지원을 위한 바운티를 걸었다는 것으로, 그 방면에서도 진전이 있기를 기대합니다!

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

우리는 마침내 100개가 넘는 메시지 스레드를 마무리했고, 두 네트워크가 무엇이며 어디에 어울리는지, 그리고 추가 협업의 여지가 어느 정도인지 더 명확하게 파악하게 되었습니다. 여기서 그들이 어떤 토폴로지나 위협 모델에 가장 적합한지까지는 들어가지 않겠지만, 더 알고 싶다면 리스트를 살펴보면 됩니다. 협업 측면에서는, 우리의 SSU transport를 재사용하기 위한 샘플 코드를 toad에게 보냈고, 이는 단기적으로 Freenet 쪽 사람들에게 도움이 될 수 있습니다. 앞으로는 I2P가 실용적인 환경에서 Freenet 사용자에게 premix 라우팅(사전 믹싱 라우팅)을 제공하기 위해 함께 작업하게 될 수도 있습니다. Freenet이 발전함에 따라, Freenet을 클라이언트 애플리케이션으로서 I2P 위에서 동작시키는 것도 가능해질 수 있으며, 이를 실행하는 사용자들 사이에서 자동화된 콘텐츠 배포(예: Syndie 아카이브와 게시물 푸시)가 가능해질 것입니다. 다만 먼저 Freenet이 계획 중인 부하 및 콘텐츠 배포 시스템이 어떻게 동작하는지 지켜볼 것입니다.

* 3) Tunnel bootstrap attacks

Michael Rogers가 I2P의 tunnel 생성과 관련된 몇 가지 흥미로운 새로운 공격에 관해 연락을 취했다[2][3][4]. 주된 공격(부트스트랩 전체 과정 동안 predecessor attack(선행자 공격)을 성공적으로 수행하는 것)은 흥미롭지만, 실제로는 그리 실용적이지 않다 - 성공 확률은 (c/n)^t이며, 여기서 c는 공격자 수, n은 네트워크의 피어 수, t는 대상이 구축한 tunnel 수(수명 전체 기준)이다 - 이는 router가 h개의 tunnel을 구축한 이후, 공격자가 하나의 tunnel 내 h개의 hop 전부를 장악할 확률(P(success) = (c/n)^h)보다도 더 낮다.

Michael이 메일링 리스트에 또 다른 공격에 관한 글을 올렸고, 현재 우리가 이를 검토하고 있으니, 그곳에서도 진행 상황을 확인하실 수 있을 것입니다.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker가 업로드 버그 해결에 더 진전을 보이고 있으며, 보고에 따르면 문제를 정확히 파악했습니다. 오늘 밤에는 CVS에 반영될 것으로 기대되며, 곧이어 0.1.1.33으로 릴리스될 예정입니다. 더 많은 정보는 포럼 [5]를 계속 확인해 주세요.

[5] http://forum.i2p.net/viewforum.i2p?f=25

소문에 따르면 redzara가 Phex 메인라인에 다시 병합하는 작업도 꽤 잘 진척되고 있다고 하니, Gregor의 도움을 받아 곧 모든 것을 최신 상태로 맞출 수 있기를 바랍니다!

* 5) Syndie/Sucker

dust도 Sucker와 함께 꾸준히 작업해 왔고, 코드로 Syndie에 더 많은 RSS/Atom 데이터를 가져오고 있다. 아마도 Sucker와 post CLI를 Syndie에 더 깊이 통합하고, 심지어 웹 기반 컨트롤로 서로 다른 RSS/Atom 피드를 다양한 블로그로 가져오는 작업을 예약할 수도 있을 것이다. 두고 보자...

* 6) ???

위에서 언급한 것들 외에도 많은 일들이 진행되고 있지만, 제가 파악하고 있는 핵심은 위와 같습니다. 질문이나 우려 사항이 있거나 다른 이야기를 하고 싶다면, 오늘 UTC 기준 오후 8시에 #i2p에서 열리는 회의에 가볍게 들러 주세요!

=jr
