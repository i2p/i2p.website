---
title: "2006-01-17자 I2P 상태 노트"
date: 2006-01-17
author: "jr"
description: "0.6.1.9에서의 네트워크 상태, tunnel 생성 암호화 개선 및 Syndie 블로그 인터페이스 업데이트"
categories: ["status"]
---

안녕하세요 여러분, 또 화요일이네요

* Index

1) 네트워크 상태 및 0.6.1.9 2) Tunnel 생성 암호화 3) Syndie 블로그 4) ???

* 1) Net status and 0.6.1.9

0.6.1.9가 출시되고 네트워크의 70%가 업그레이드되면서, 포함된 버그 수정 대부분은 예상대로 동작하는 것으로 보이며, 새 속도 프로파일링이 좋은 피어들을 잘 골라내고 있다는 보고가 있습니다. 빠른 피어에서는 CPU 사용량 50~70%로 300KBps를 넘는 지속 처리량이 보고되었고, 다른 router들은 100~150KBps 범위에 있으며, 더 낮은 쪽은 1~5KBps를 겨우 밀어주는 정도까지 떨어집니다. 다만 여전히 router의 ID 변동이 상당해서, 이를 줄일 것이라 생각했던 버그 수정은 효과가 없었던 듯합니다(아니면 그 변동이 정당한 것일 수도 있습니다).

* 2) Tunnel creation crypto

가을에는 우리가 tunnel(터널)을 어떻게 구축할지, 그리고 Tor 스타일의 텔레스코핑 방식 tunnel 생성과 I2P 스타일의 탐색적 tunnel 생성 간의 트레이드오프에 관해 많은 논의가 있었다 [1]. 그 과정에서 우리는 조합[2]을 고안했는데, 이는 Tor 스타일의 텔레스코핑 방식 생성[3]의 문제를 제거하고, I2P의 단방향성 이점을 유지하며, 불필요한 실패를 줄인다. 당시에는 다른 일들이 많아 그 새로운 조합의 구현이 미뤄졌지만, 이제 0.6.2 릴리스를 앞두고 있고 그 기간에는 어차피 tunnel 생성 코드를 개편해야 하므로, 이제 이를 매듭지을 때다.

며칠 전에 새로운 tunnel 암호 방식의 초안 명세를 대략 작성해 내 syndie 블로그에 올렸고, 실제로 구현하는 과정에서 드러난 사소한 변경을 거친 뒤, CVS [4]에 명세를 정리해 두었습니다. 이를 구현한 기본 코드도 CVS [5]에 있지만, 아직 실제 tunnel 구축에 연결되어 있지는 않습니다. 혹시 시간이 되신다면, 그 명세에 대한 피드백을 주시면 감사하겠습니다. 한편, 저는 새로운 tunnel 구축 코드 작업을 계속하겠습니다.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html 그리고     부트스트랩 공격과 관련된 스레드를 참고하세요 [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

앞서 언급했듯이, 이번 새로운 0.6.1.9 릴리스에는 Syndie 블로그 인터페이스에 상당한 개편이 이루어졌으며, cervantes의 새로운 스타일과 각 사용자별 블로그 링크 및 로고 선택 기능이 포함됩니다 (e.g. [6]). 프로필 페이지에서 "configure your blog" 링크를 클릭하면 왼쪽에 있는 링크들을 관리할 수 있으며, http://localhost:7657/syndie/configblog.jsp 로 이동합니다. 거기에서 변경을 완료하면, 다음에 게시물을 아카이브로 푸시할 때 그 정보가 다른 사람들에게 제공됩니다.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

이미 회의에 20분이나 늦었으니, 짧게 하겠습니다. 다른 일들도 몇 가지 진행 중인 건 알지만, 여기서 다 공개하기보다는 논의하고 싶은 개발자들은 회의에 와서 제기해 주세요. 아무튼, 일단은 여기까지, 다들 #i2p에서 봐요!

=jr
