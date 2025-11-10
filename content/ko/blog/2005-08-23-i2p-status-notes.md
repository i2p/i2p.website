---
title: "2005-08-23자 I2P 상태 노트"
date: 2005-08-23
author: "jr"
description: "0.6.0.3 릴리스 개선 사항, Irc2P 네트워크 상태, i2p-bt용 susibt 웹 프런트엔드, 그리고 Syndie 보안 블로깅을 다루는 주간 업데이트"
categories: ["status"]
---

여러분 안녕하세요, 다시 주간 진행 상황 노트를 공유할 시간입니다

* Index

1) 0.6.0.3 상태 2) IRC 상태 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

며칠 전에 언급했듯이[1], 새 0.6.0.3 릴리스를 공개했고, 지금 바로 즐기실 수 있습니다. 이는 0.6.0.2 릴리스에 비해 큰 개선입니다(irc에서 끊김 없이 며칠씩 접속이 유지되는 일도 드물지 않습니다 - 저도 업그레이드 때문에 중단되기 전까지 5일 업타임을 경험했습니다), 하지만 몇 가지 주목할 만한 점이 있습니다. 그래도 항상 그런 것은 아닙니다 - 네트워크 연결이 느린 분들은 문제를 겪기도 하지만, 그래도 진전입니다.

피어 테스트 코드에 대해 (매우) 흔히 나오는 질문이 하나 있습니다- "왜 Status: Unknown이라고 표시되나요?" Unknown은 *완전히 정상입니다* - 이것이 문제가 있다는 뜻은 절대 아닙니다. 또, 상태가 가끔 "OK"와 "ERR-Reject" 사이를 오가는 것을 보더라도, 그렇다고 해서 괜찮다는 뜻은 아닙니다 - 만약 한 번이라도 ERR-Reject가 보인다면, NAT 또는 방화벽 문제일 가능성이 매우 높다는 뜻입니다. 혼란스러운 거 알아요, 그리고 상태 표시를 더 명확하게 하고 (가능한 경우 자동으로 해결하는) 릴리스를 나중에 제공할 예정이지만, 당분간은 여러분이 "헉 고장났어!!!11 상태가 Unknown이야!"라고 말해도 제가 무시하더라도 놀라지 마세요 ;)

(과도하게 많은 'Unknown' 상태 값의 원인은, 우리가 이미 SSU 세션을 맺고 있는 상대가 "Charlie" [2]인 피어 테스트를 무시하고 있기 때문이며, 이는 설령 우리 NAT(네트워크 주소 변환)가 제대로 작동하지 않더라도 그들이 우리 NAT를 통과할 수 있음을 의미합니다)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

앞서 언급했듯이, Irc2P 운영자들은 네트워크를 훌륭하게 운영하고 있으며 지연 시간은 크게 줄고 신뢰성은 크게 높아졌습니다 - 며칠째 netsplit(IRC 서버 간 연결 분리 현상)을 보지 못했습니다. 또한 그쪽에는 새로운 IRC 서버가 하나 더 생겨 이제 총 3개입니다 - irc.postman.i2p, irc.arcturus.i2p, 및 irc.freshcoffee.i2p. 혹시 Irc2P 측에서 회의 중에 진행 상황을 업데이트해 주실 수 있을까요?

* 3) susibt

susimail로 유명한 susi23이 BT(비트토렌트) 관련 도구 두 가지 - susibt [3]와 새로운 트래커 봇 [4]을 들고 돌아왔습니다. susibt는 i2p-bt의 동작을 관리하기 위한 웹 애플리케이션(여러분의 i2p jetty 인스턴스에 손쉽게 배포 가능)입니다. 그녀의 사이트에 따르면:

SusiBT는 i2p-bt를 위한 웹 프런트엔드입니다. 이는 귀하의 i2p router에 통합되어 자동 업로드/다운로드, 재시작 후 작업 이어서 진행, 그리고 파일 업로드/다운로드와 같은 일부 관리 기능을 제공합니다. 애플리케이션의 이후 버전에서는 토렌트 파일의 자동 생성 및 업로드를 지원할 예정입니다.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

"w00t" 한 번 들려줄 수 있나요?

* 4) Syndie

메일링 리스트와 채널에서 언급했듯이, 보안되고 인증된 블로깅/콘텐츠 배포를 위한 새로운 클라이언트 앱이 나왔습니다. Syndie를 사용하면 사이트가 다운되어 있어도 콘텐츠를 읽을 수 있으므로, '당신의 eepsite(I2P Site)가 지금 살아 있나요'라는 질문은 사라집니다. 또한 Syndie는 프론트엔드에 집중함으로써 콘텐츠 배포 네트워크에 내재한 온갖 골치 아픈 문제들을 피해 갑니다. 어쨌든 아직 한창 개발 중이지만, 직접 들어가 써 보고 싶다면 http://syndiemedia.i2p/ 에 공개 Syndie 노드가 있습니다 (웹에서는 http://66.111.51.110:8000/ 로도 접속할 수 있습니다). 마음껏 들어가 블로그를 만들거나, 모험심이 생긴다면 댓글/제안/우려 사항을 블로그에 올려 보세요! 물론 패치도 환영이지만 기능 제안 역시 환영합니다. 그러니 마음껏 의견을 보내 주세요.

* 5) ???

Saying lots going on is a bit of an understatement... beyond the above, I'm hacking on some improvements to SSU's congestion control (-1 is in cvs already), our bandwidth limiter, and the netDb (for the occational site unreachability), as well as debugging the CPU issue reported on the forum. I'm sure others are hacking on some cool things to report as well, so hopefully they'll swing by the meeting tonight to rant away :)

어쨌든, 오늘 밤 GMT 기준 오후 8시에 평소 사용하는 서버의 채널 #i2p에서 만나요!

=jr
