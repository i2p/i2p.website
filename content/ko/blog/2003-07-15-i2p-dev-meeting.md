---
title: "I2P 개발자 회의"
date: 2003-07-15
author: "nop"
description: "프로젝트 업데이트 및 기술 논의를 다루는 I2P 개발 회의"
categories: ["meeting"]
---

(웨이백 머신 제공 http://www.archive.org/)

## 간단 요약

<p class="attendees-inline"><strong>참석자:</strong> gott, hezekiah, jeremiah, jrand0m, mihi, Neo, nop, WinBear</p>

## 회의 기록

<div class="irc-log"> --- 로그 시작 Tue Jul 15 17:46:47 2003 17:46 < gott> 안녕. 17:46 <@nop> 제가 조용했던 건 미리 말씀드리려고요 17:46 <@hezekiah> Tue Jul 15 21:46:49 UTC 2003 17:47 <@hezekiah> 좋아요. iip-dev 회의가 시작되었습니다. 17:47 <@hezekiah> 48번째인가 49번째인가요? 17:47 < jrand0m> nop> 그래서 우리가 router 아키텍처를 최대한 빨리 확정하는 게 중요하다는 거죠. 사람마다 	속도가 다르다는 걸 이해하고, 각 구성요소가 각자 진행할 수 있도록 분할해야 합니다 17:47 < mihi> 49번째 17:47 <@hezekiah> 좋아요! 제49회 iip-dev 회의에 오신 걸 환영합니다! 17:47 < jrand0m> 직장에서 3일만 더 일하면, 그 이후에는 주 90시간 이상을 	이걸 진행하는 데 투입할 겁니다 17:48 < jrand0m> 모두가 그렇게 할 수 있으리라 기대하진 않아요. 	그래서 분할이 필요하다는 거죠 17:48 < jrand0m> 안녕 hezekiah :) 17:48 <@hezekiah> ㅋㅋ 17:48 <@nop> 거기에 반박하자면 17:48 <@hezekiah> 잠시 기다릴게요. 그다음에 안건으로 넘어가죠. :) 17:48 <@nop> router 아키텍처의 보안은 서두르지 않는 것에도 	달려 있습니다 17:49 <@nop> 만약 우리가 서두르면 17:49 <@nop> 간과하게 되고 17:49 <@nop> 나중에 큰 수습을 하게 될 수도 있습니다 17:49 -!- Rain [Rain@anon.iip] 님이 나갔습니다 [I Quit] 17:49 < jrand0m> nop> 동의하지 않음. router를 구현하지 않고도(심지어 	네트워크가 어떻게 동작할지 몰라도) 앱 레이어와 API들은 만들 수 있어요 17:49 <@nop> 그건 동의 17:50 <@nop> 저는 특히 하부 네트워크를 말하는 겁니다 17:50 < jrand0m> 제가 보낸 API에 합의할 수 있다면, 그게 우리가 필요한 	분할입니다 17:50 < jrand0m> 맞아요, router 구현과 네트워크 설계는 아직 안 끝났죠 17:50 <@nop> 오케이 17:50 <@nop> 오, 지금까지의 당신 API에는 확실히 동의해요 17:51 <@hezekiah> jrand0m: 한 가지 문제. 17:51 < jrand0m> 말해봐 hezekiah 17:51 <@hezekiah> C로 구현하면 모양이 달라질 거예요. 17:51 < jrand0m> 그렇게 많이 다르진 않아요 17:51 < gott> 이런 17:51 < jrand0m> 대문자가 좀 줄고, 오브젝트를 struct로 대체하면 되죠 17:51 < gott> 어떤 언어로 구현을 고려하고 있나요? 17:51 < jrand0m> (API에 대해) 17:51 <@hezekiah> 어, jrand0m? C에는 'byte[]'가 없어요. 17:51 < jrand0m> gott> 그에 대한 몇 가지 예시는 메일 아카이브를 읽어봐요 17:52 <@hezekiah> 아마 길이를 지정하는 정수와 함께 void*를 쓰게 될 거예요. 17:52 < jrand0m> hezekiah> 그럼 unsigned int[] 17:52 < gott> jrand0m: 간만에 내가 끼지 않는 종교 전쟁이네 17:52 <@hezekiah> 제 기억이 맞다면(여기서 좀 도와줘요, nop), 	함수에서 unsigned int[]를 그대로 반환하진 못해요. 17:53 <@hezekiah> gott: 뭐하고 비교해서요? 의사코드? 17:53 < jrand0m> 맞아요, 문법적 차이죠. 하지만 진짜 차이가 있다면, 	최대한 빨리 해결해야 해요. (가령 오늘) 아마 지금이 "high level 	router architecture and API"라는 제목의 제가 보낸 이메일을 보고 	검토하기 좋은 때일 거예요? 17:54 <@hezekiah> nop? UserX? 할 마음 있나요? 17:54 < jrand0m> 많이 다르진 않지만 어쨌든 다르죠. 	그래서 오늘 이메일에서 Java API라고 한 거예요 :) 17:54 -!- WinBear [WinBear@anon.iip] 님이 #iip-dev에 입장했습니다 17:55 <@nop> 잠깐만 17:55 <@nop> 위에 읽는 중 17:55 -!- mihi_2 [~none@anon.iip] 님이 #iip-dev에 입장했습니다 17:55 -!- mihi 닉이 nickthief60234 로 변경되었습니다 17:55 -!- mihi_2 닉이 mihi 로 변경되었습니다 17:55 < jrand0m> 어서 와, mihi 17:55 < gott> 그나저나, 이거 실시간 로그 남기고 있나요? 17:55 -!- nickthief60234 [~none@anon.iip] 님이 나갔습니다 [EOF From client] 17:55 <@hezekiah> gott: 네. 17:55 < mihi> 중복은 진리 ;) 17:55 < gott> 그럼 나중에 읽을게요. 17:55 -!- gott [~gott@anon.iip] 님이 #iip-dev를 떠났습니다 [gott] 17:56 <@nop> 오케이 17:56 <@nop> 네 17:56 < WinBear> jrand0m: 안녕 17:56 <@nop> 확실히 차이가 있어요 17:56 <@nop> 우리가 필요한 건 17:56 < jrand0m> 안녕, WinBear 17:56 <@nop> 각 언어에 대해 주요 API 레벨 컨트롤을 작성할 	개발자 팀입니다 17:56 <@nop> jrand0m은 Java를 맡을 수 있다는 걸 알고 있고 17:56 <@nop> 아마 thecrypto와도 팀을 이룰 수 있겠죠 17:56 <@nop> 그리고 hezekiah와 팀은 C를 할 수 있고 17:56 <@nop> 그리고 jeremiah가 원한다면 17:56 <@nop> Python을 할 수 있고 17:56 <@hezekiah> 저 C++도 할 수 있어요! ;-) 17:56 <@nop> 오케이 17:56 <@nop> C++도 함께 17:57 <@hezekiah> ㅋㅋ 17:57 <@nop> C++도 아마 17:57 <@nop> C와 함께 쓸 수 있을 거예요 17:57 <@nop> 템플릿을 과하게 쓰지 않는다면 17:57 < jrand0m> ㅎㅎ 17:57 <@hezekiah> ㅋㅋ 17:57 <@hezekiah> 사실, MSVC는 C와 C++ 오브젝트 파일을 	링크할 수 있지만, gcc는 그걸 좋아하지 않는 것 같아요. 17:57 <@nop> 즉, C와 호환되는 struct만 고수하라는 건데, 	그게 가능하지 않나요 17:57 < jrand0m> 그 전에 첫 질문은, 어떤 애플리케이션들이 	이 API들을 사용할 건가요? Java를 쓰고 싶어하는 앱들은 알고 있고, iproxy는 C로 갈까요? 17:58 <@hezekiah> C와 C++이 오브젝트 호환된다고는 생각하지 않아요. 17:58 <@nop> 오케이 17:58 <@hezekiah> C++이 C와 잘 맞는 정도가 Java보다 	크게 낫지는 않을 거예요. 17:58 <@nop> 그럼 UserX가 C를 맡고 17:58 <@nop> 당신이 C++을 맡을 수도 있겠네요 17:58 <@hezekiah> We don 17:58 <@nop> ? 17:58 <@hezekiah> 원하지 않으면 C++을 _할_ 필요도 없어요. 단지 	제가 선호할 뿐이죠. 17:59 <@nop> 음, 문제는 17:59 <@nop> C++ 개발자가 많다는 거죠 17:59 <@nop> 특히 마이크로소프트 세계에는 17:59 <@hezekiah> 리눅스 세계에서도요.(참고: KDE와 Qt.) 17:59 < jrand0m> C와 C++은 .so나 .a만 만들면 바이너리 호환돼요 17:59 < jrand0m> (참고로) 18:00 <@nop> C가 C++의 대체가 될 수 있을까요? 즉, C++ 개발자가 	C 개발자가 만든 C++ API보다 C API를 다루는 게 더 쉬울까요? 18:00 <@hezekiah> jrand0m: 네. 라이브러리는 아마 가능할 거예요 ... 하지만 	만약 18:00 <@hezekiah> jrand0m: 클래스를 쓸 수조차 없다면, 다소 	목적에 어긋나죠. 18:00 <@nop> 그렇죠 18:00 <@nop> C로 가죠 18:01 <@nop> C++ 코더도 C 라이브러리는 비교적 쉽게 	호출할 수 있으니까요 18:01 <@hezekiah> 한 모듈이 다른 모듈의 함수를 호출해야 한다면, 	둘 다 같은 언어인 게 가장 좋습니다. 18:01 <@hezekiah> nop: C++ 코더는 C를 충분히 알겠죠... 다만 	C를 따로 /배운/ 적이 없다면 좀 고생할 수 있어요. 18:02 <@hezekiah> 하지만 C는 C++의 부분집합에 불과하니, C 코더가 	C++을 안다고 보긴 어렵죠. 18:02 -!- logger_ [~logger@anon.iip] 님이 #iip-dev에 입장했습니다 18:02 -!- #iip-dev 주제: 회의 후 로그파일이 온라인에 올라갑니다: 	http://wiki.invisiblenet.net/?Meetings 18:02 [Users #iip-dev] 18:02 [@hezekiah] [+Ehud    ] [ leenookx] [ moltar] [ tek    ] 18:02 [@nop     ] [ jeremiah] [ logger_ ] [ Neo   ] [ WinBear] 18:02 [@UserX   ] [ jrand0m ] [ mihi    ] [ ptsc  ] 18:02 -!- Irssi: #iip-dev: Total of 14 nicks [3 ops, 0 halfops, 1 voices, 10 normal] 18:02 < jrand0m> 맞아요 18:02 -!- Irssi: Join to #iip-dev was synced in 9 secs 18:02 < jrand0m> (JMS와 함께 :) 18:02 <@nop> 예 18:03 -!- 이제부터 당신의 닉은 logger 입니다 18:03 < jrand0m> 좋아요, 우선 전체 아키텍처를 검토해서 	이 API들이 실제로 관련성이 있는지 볼 수 있을까요? 18:03 <@nop> 좋아요  18:04 < jrand0m> :) 18:04 < jrand0m> 좋아요, 제가 보낸 routerArchitecture.png가 	첨부된 이메일을 보세요. 그 분리 방식에 대한 의견 있나요? 18:04 -!- tek [~tek@anon.iip] 님이 나갔습니다 [] 18:05 < WinBear> jrand0m: 그거 위키에 있나요? 18:05 < jrand0m> WinBear> 아뇨, 메일링 리스트에 있어요, 다만 아카이브가 	내려가 있어요. 위키(wikki)에 추가해볼게요 18:06 <@hezekiah> 제가 틀렸다면 정정해 주세요 ... 18:07 <@hezekiah> ... 가능한 한 비슷하게 맞춘 API가 3개 필요해 보입니다. 18:07 <@hezekiah> 맞나요? 18:07 < jrand0m> 네 hezekiah 18:07 <@hezekiah> 각 API가 서로 다른 언어라면, 각각 별도의 구현을 	갖게 되나요? 18:07 < jrand0m> 네 18:07 <@hezekiah> 아니면 Java나 Python이 C 라이브러리에 접근할 방법이 있나요? 18:08 < jrand0m> 네, 있지만 그 길로 가고 싶진 않아요 18:08 < mihi> Java의 경우: JNI 18:08 <@hezekiah> 그럼 Java, C, C++, Python 등이 함께 동작한다는 얘기는 	무의미한 건가요? 어차피 함께할 일이 없을 테니? 18:08 < jrand0m> 위키에 이미지는 어떻게 첨부하죠? 18:08 <@hezekiah> 각 API는 해당 언어로 작성된 자체 백엔드를 가집니다. 18:08 < jrand0m> 아니에요 hezekiah, 다이어그램을 보세요 18:09 <@hezekiah> 아, 그렇네! 18:09 <@hezekiah> API는 백엔드에 링크되지 않아요. 18:10 <@hezekiah> 소켓으로 통신합니다. 18:10 < jrand0m> 예, 그럼요 18:10 <@hezekiah> 그래도 아직 좀 헷갈리네요. 18:10 <@hezekiah> 잠깐만요. :) 18:11 <@hezekiah> 좋아요. 'transport'라고 표시된 건 뭐죠? 18:11 < jrand0m> 예를 들어, 양방향 HTTP 트랜스포트, SMTP 트랜스포트, 	일반 소켓 트랜스포트, 폴링 HTTP 소켓 등 18:11 < jrand0m> router들 사이에서 바이트를 옮기는 것 18:12 <@hezekiah> 좋아요. 18:12 <@hezekiah> 그러면 제가 보고 있는 다이어그램은 한 사람의 컴퓨터를 보여주는 거네요. 18:12 <@hezekiah> 그 사람은 트랜스포트를 통해 다른 사람들의 컴퓨터와 	통신하는 router를 가지고 있고요. 18:12 < jrand0m> 맞아요 18:12 <@hezekiah> 사람 1(앨리스)은 애플리케이션을 두 개 실행 중입니다. 18:12 <@hezekiah> 하나는 C로, 다른 하나는 Java로 되어 있고요. 18:13 <@hezekiah> 둘 다 라이브러리에 링크되어 있어요(그게 API). 18:13 < jrand0m> 둘 다 각각 다른 라이브러리(API)에 '링크'되어 있어요 18:13 <@nop> 간단한 개념이죠 18:13 <@nop> 네 18:13 <@hezekiah> 그 라이브러리들이 프로그램의 입력을 받아 암호화하고, 	소켓(유닉스 소켓 또는 TCP)으로 router에 보냅니다. ... 그 router도 앨리스가 	실행 중인 또 다른 프로그램이죠. 18:13 < jrand0m> 맞아요 18:14 <@hezekiah> 좋아요. 그러니까 isproxy를 둘로 나눈 것과 비슷하네요. 18:14 < jrand0m> 정답 :) 18:14 <@hezekiah> 한쪽은 저수준 부분으로 C로 작성되고, 다른 한쪽은 	고수준 부분으로 어떤 언어로든 작성되는 거죠. 18:14 < jrand0m> 정확해요 18:14 <@hezekiah> 좋아요. 이해했어요. :) 18:14 < jrand0m> w00t 18:14 <@hezekiah> 그래서 어떤 언어도 다른 언어와 잘 지낼 필요가 없네요. 18:14 < jrand0m> WinBear> 미안, 위키가 텍스트만 받아서 	거기엔 올릴 수 없네요 :/ 18:15 <@hezekiah> 모두 소켓을 통해 router와 통신하니, 설계 관점에서는 	PASCAL로 API를 써도 상관없죠. 18:15 <@nop> 네 18:15 <@nop> 임의의 18:15 < jrand0m> 맞아요 18:15 <@nop> 임의의 소켓을 처리합니다 18:15 < jrand0m> 다만 몇 가지는 표준화해야 해요(예: 	Destination, Lease 등의 데이터 구조) 18:15 < WinBear> hezekiah가 말하는 걸로 대충 이해한 것 같아요 18:15 < jrand0m> 굿 18:16 <@hezekiah> jrand0m: 맞아요. 그 소켓을 통해 오가는 바이트의 	구조와 순서는 어딘가 설계에 정의되어 있죠 18:16 <@hezekiah> 어디선가요. 18:17 <@hezekiah> 하지만 그 바이트를 송수신하는 방식은 원하는 대로 	즐겁게 구현할 수 있어요. 18:17 <@nop> WinBear: irc 클라이언트가 isproxy와 동작하는 방식과 	정확히 같아요 18:17 < jrand0m> 맞습니다 18:17 <@hezekiah> 좋아요. 18:17 <@hezekiah> 이제 이해했어요. :) 18:17 -!- moltar [~me@anon.iip] 님이 #iip-dev를 떠났습니다 [moltar] 18:17 <@nop> 글쎄요 18:17 <@nop> 완전히 같진 않죠 18:17 <@hezekiah> 어라. 18:17 <@nop> 하지만 그게 어떻게 동작하는지 떠올리면 18:17 <@nop> 임의 소켓을 이해할 수 있어요 18:17 <@nop> isproxy는 단지 라우팅하고 18:17 <@nop> 전달할 뿐이에요 18:18 <@nop> 이제 jrand0m 18:18 <@nop> 빠른 질문 하나 18:18 < jrand0m> 예, 그럼요? 18:18 <@nop> 이 API는 이 네트워크에서 동작하도록 새로 설계된 	새 애플리케이션만을 위한 건가요 18:18 -!- mode/#iip-dev [+v logger] by hezekiah 18:18 < WinBear> nop: 고수준 부분이 irc 클라이언트를 대체하는 건가요? 18:18 < jrand0m> nop> 네. 다만 SOCKS5 프록시도 이 API를 사용할 수 있어요 18:18 <@nop> 아니면 이미 표준 클라이언트를 위한 중간자도 	가능한가요 18:18 <@nop> 예를 들면 18:19 <@nop> 그래서 우리가 해야 할 건 중간자 -> api만 	작성하면 되게 18:19 < jrand0m> (하지만 'lookup' 서비스는 없다는 점에 유의하세요 - 	이 네트워크엔 DNS가 없습니다) 18:19 < jrand0m> 맞아요 18:19 <@nop> 그래서 모질라 같은 걸 지원할 수 있게 18:19 <@nop> 그들은 플러그인만 코딩하면 되게 18:19 < jrand0m> nop> 네 18:19 <@nop> 오케이 18:19 <@nop> 아니면 트랜스포트 :) 18:20 < jrand0m> (예: SOCKS5는 HTTP 아웃프록시를 	destination1, destination2, destination3로 하드코딩) 18:20 <@nop> 오케이 18:20 < WinBear> 이해한 것 같아요 18:21 < jrand0m> w00t 18:21 < jrand0m> 이 설계에서 고민했던 것 중 하나는 개인 키를 	앱의 메모리 공간에 유지하는 것이었습니다 - router는 	destination 개인 키를 절대 다루지 않습니다. 18:21 <@hezekiah> 그러면 애플리케이션은 데이터를 API로 보내기만 하면 	I2P 네트워크를 통해 원시 데이터가 전송되고, 나머지는 신경 쓸 필요가 없다는 거죠. 18:22 <@hezekiah> 맞죠? 18:22 < jrand0m> 즉 API들이 종단 간 암호화 부분을 	구현해야 한다는 뜻이죠 18:22 < jrand0m> 정확해요 hezekiah 18:22 <@hezekiah> 좋아요. 18:22 <@nop> 네 18:22 <@nop> 그게 취지예요 18:22 <@nop> 그걸 대신 처리해주죠 18:22 <@nop> 여러분은 훅만 호출하면 됩니다 18:23 <@hezekiah> 빠른 질문 하나만: 18:23 <@hezekiah> 이 'router'는 분명히 각 트랜스포트 위에서 	특정 프로토콜을 말해야 하죠. 18:23 < jrand0m> 맞아요 18:23 <@hezekiah> 그럼 router의 여러 구현을 제공하는 것도 	가능하겠네요 ... 18:23 < jrand0m> 네 18:24 <@hezekiah> ... 동일한 프로토콜을 사용하기만 한다면요. 18:24 < jrand0m> (그래서 스펙에 bitbucket에 대한 placeholder가 있어요) 18:24 < jrand0m> 맞습니다 18:24 <@hezekiah> 그러면 Java로 된 router, C로 된 router, 	PASCAL로 된 router가 있을 수 있고요. 18:24  * jrand0m 몸서리침 18:24 < jrand0m> 하지만 그렇죠 18:24 <@hezekiah> 그리고 TCP/IP 위에서 같은 프로토콜로 대화하니 	서로 통신할 수 있죠. 18:24  * WinBear 깜짝 놀람 18:24 <@hezekiah> jrand0m: 맞아요. 저도 PASCAL 하던 시절이 	그리 달갑진 않네요. 18:25 < jrand0m> 음, 예를 들어 Pascal은 TCP 트랜스포트를 통해 C 쪽과 	대화하고, C는 HTTP 트랜스포트를 통해 Java 쪽과 대화할 수 있죠 18:25 <@hezekiah> 맞아요. 18:25 < jrand0m> (트랜스포트는 같은 종류의 트랜스포트끼리 통신하고, 	router는 그 사이에서 전달되는 메시지를 관리하지만 전달 방식 자체는 다루지 않습니다) 18:26 <@hezekiah> 제가 말하고 싶었던 요점은, 프로토콜이 같다면 	router가 어떤 언어로 구현되었는지는 상관없다는 겁니다. 18:26 < jrand0m> 맞아요 18:26 <@hezekiah> 굿. 18:26 < jrand0m> 이제 C 대 Java 등등의 논쟁에 제가 '상관없어'라고 	한 이유를 이해하겠죠?  :) 18:26 <@hezekiah> 네. 18:26 <@hezekiah> ㅋㅋ 18:27 <@hezekiah> jrand0m, 인정합니다. 이건 개발자들이 이 네트워크용 	프로그램을 작성하기 아주 편하게 해줄 겁니다. 18:27 < jrand0m> 헤, 뭐, API가 완전히 독창적인 건 아니에요. 	이게 Message Oriented Middleware(MOM)가 동작하는 방식이거든요 18:27 <@hezekiah> 그리고 특정 플랫폼 특화 기능(예: 64비트 CPU)에 	특화된 router를 만들 수도 있어요. 18:28 < jrand0m> 물론이죠 18:28 <@hezekiah> jrand0m: 겸손하기까지! ;-) 18:28 <@hezekiah> 좋아 보입니다. 18:28 < jrand0m> 좋아요, UserX, nop, 이 분리가 말이 되나요? 18:28 <@nop> 물론이죠 18:28 <@nop> userx 아직 있나요 18:29 <@hezekiah> 1:26 동안 자리 비움 상태예요. 18:29 < jrand0m> 'ㅇㅋ. 그럼 작업이 두 가지네요: 네트워크 설계, 그리고 	API 동작 방식 설계. 18:29 <@nop> 맞아요 18:29 <@hezekiah> 빠르고 간단한 질문: API는 종단 간 암호화를 합니다. 	router들은 노드 간 암호화를 하나요 ? 18:29 <@nop> 네 18:30 < jrand0m> 네 18:30 < jrand0m> (트랜스포트 레벨) 18:30 <@hezekiah> 좋아요. :) 18:30 <@nop> hezekiah: 그 점은 지금까지 우리가 가진 것과 	매우 비슷해요 18:30 <@nop> 그 측면에서 18:31 < jrand0m> 좋아요.. 어, 젠장, 성능 모델에 대한 코멘트는 	thecrypto가 없네요. 18:31 < Neo> 그리고 보안 성향이 강한 사람들을 위해, 앱이 API로 	보내기 전에 PGP 암호화를 할 수도 있죠 ;) 18:31 < jrand0m> 물론이죠, Neo 18:31 < jrand0m> 종단 간 암호화를 API에서 아예 빼고 	앱에 맡길까도 고민했어요... 18:31 <@hezekiah> jrand0m: 그건 너무 가혹하죠. 18:31 < jrand0m> 헤헤 18:32 <@hezekiah> 참고로, API와 router는 소켓으로 통신합니다. 18:32 <@hezekiah> 유닉스에선 UNIX 소켓을 쓸까요, 아니면 로컬 TCP/IP 	소켓을 쓸까요? 18:32 < jrand0m> 아마 단순화를 위해 로컬 TCP/IP만 쓸 듯 18:32 <@nop> 잠깐만요 18:32 <@hezekiah> (둘 다 받는 router를 만들 수도 있겠죠.) 18:33  * hezekiah 는 이런 교체 가능한 부품식 구성이 정말 마음에 듭니다 18:33 <@nop> 잠시만요 18:34 <@hezekiah> 기다리는 중 ... :) 18:34 <@nop> 집에 있는 thecrypto에게 전화해볼게요 18:34 <@nop> 접속할 수 있는지 보죠 18:34 < jrand0m> 좋죠 18:34 <@hezekiah> ㅋㅋ 18:34  * hezekiah 두꺼운 이탈리아 억양 장착 18:34 <@hezekiah> Nop한테는 ... 인맥이 있다구! 18:34 < jeremiah> 하이 18:34 <@nop> 안녕 jeremiah 18:35 < jrand0m> 안녕 jeremiah 18:35 <@nop> API 레벨에서 파이썬 API 도와줄 수 있겠어요? 18:35 < jeremiah> 물론이요 18:35  * jeremiah 백로그 읽는 중 18:35 < jrand0m> 좋군요 18:35  * nop 통화 중 18:36 <@nop> 집에 없대요 18:36 <@nop> 한 시간 뒤에 온다고 합니다 18:36 < jrand0m> 'ㅇㅋ, 다른 분들 .xls 읽어보셨거나 	모델에 대한 코멘트 있나요? 18:37 <@hezekiah> .xls는 읽었는데... p2p를 잘 몰라서 	대부분 이해하지 못했어요. 18:37 <@hezekiah> 그런 건 UserX가 잘하죠. 18:37 <@nop> 저는 아직 읽어봐야 해요 18:37 < jrand0m> (그나저나, morphmix 수치가 엄청나더군요... 	무작위 호스트의 평균 핑이 20~150ms 정도라고 했어요, 	저는 3-500을 예상했는데) 18:37 < jrand0m> 굿 18:37 <@nop> 스타오피스인가요, 오픈오피스인가요? 18:37 < jrand0m> OpenOffice인데, .xls로 내보냈어요 18:37 <@nop> 그게 엑셀이죠? 18:37 < jrand0m> 맞아요 18:38 <@hezekiah> 그런데 API 관련해서 ... 18:38 < jrand0m> 예, 그럼요? 18:38 <@hezekiah> ... C에선 boolean은 int가 되겠죠. 18:38 <@nop> 어느 이메일요 18:38 <@nop> hezekiah: 그렇죠 18:38 <@hezekiah> 클래스는 구조체 포인터로 보내야겠죠. 18:38 <@nop> boolean을 typedef하지 않는 한요 18:39 <@hezekiah> 그리고 byte[]를 쓰는 함수는 버퍼 길이를 	지정하는 추가 매개변수와 함께 void*를 써야겠죠. 18:39 <@nop> hezekiah: 좀 깐깐하네요 :) 18:39 < jrand0m> nop> 아카이브에 접근할 수가 없어서 제목이 	뭐였는지 모르겠네요, 지난주에 보낸 거였어요... 18:39 <@nop> 그건 나중으로 미뤄요 18:39 <@hezekiah> nop: 깐깐해요? 18:39 < jrand0m> 네, C API 작업하실 분들이 그 디테일은 	정리해주시면 돼요 18:39  * jeremiah 백로그 읽기 완료 18:39 <@nop> 파일 이름이 뭐죠 18:39 <@hezekiah> nop: jrand0m이 말한 대로 다듬으려면, 	달라지는 부분을 다 찾으려는 거예요. 18:40 <@hezekiah> 도움이 되고 싶어서요. :) 18:40 <@nop> hezekiah: 네, 아마 회의 시간 밖에 18:40 < jrand0m> nop> simple_latency.xls 18:40 <@hezekiah> boolean sendMessage(Destination dest, byte[] payload); 18:40 <@hezekiah>  would be 18:40 <@hezekiah> int sendMessage(Destination dest, void* payload, int length); 18:40 <@hezekiah> . 18:40 <@hezekiah> byte[]  recieveMessage(int msgId); 18:40 <@hezekiah>  that could either be: 18:41 <@hezekiah> void*  recieveMessage(int msgId, int* length); 18:41 <@hezekiah>  or 18:41 <@nop> jrand0m: 받았어요 18:41 <@hezekiah> void recieveMessage(int msgId, void* buf, int* length); 18:41 <@hezekiah>  or 18:41 < jrand0m> hezekia: why not typedef struct { int length; void* data; 	} Payload; 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId)l 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId); 18:41 < jeremiah> 그 .xls는 어디 있죠? 18:41 <@nop> 아 iip-dev 18:41 <@hezekiah> jrand0m: 방금 말한 그 struct가 기본적으로 	DataBlock이에요. 18:42 < jrand0m> 맞아요 hezekiah 18:42 <@nop> 제목은 'more models' 18:42 <@hezekiah> 아마 C 버전에는 DataBlock이 있을 거예요. 18:43 <@hezekiah> 그 외에 기억할 점은, 각 'interface'가 단지 	함수 집합이라는 겁니다. 18:43 <@hezekiah> nop: C API에서 생길 차이점을 제가 다 찾은 걸까요? 18:43 < jrand0m> 맞아요. 	아마 #include "i2psession.h" 같은 거 18:43 < jeremiah> Python API 목업이 있나요? 18:44 < jrand0m> 아니요 jeremiah, 제가 Python을 잘 몰라서요 :/ 18:44 <@nop> Java API를 다시 검토해야겠지만, 말씀하신 게 	정확하다고 봐요 18:44 < jrand0m> 하지만 Python이 OO라서 아마 Java와 비슷할 거예요 18:44 < jeremiah> 좋아요, C 버전에서 하나 파생시킬 수 있어요 18:44  * nop 은 자바쟁이는 아니라서 18:44 < jrand0m> 굿, jeremiah 18:44 < jeremiah> 며칠 전에 보낸 게 C API였나요? 18:44 <@hezekiah> 네. Python도 Java API를 처리할 수 있을 거예요. 18:44 < jrand0m> jeremiah> 그건 Java 버전이었어요 18:45 < jrand0m> 아, Java 버전은 오늘 거였고 18:45 < jrand0m> 예전 건 언어 독립적이었죠 18:45 <@hezekiah> 흠 18:45 <@nop> UserX가 C API를 도울 수 있을 거라고 하네요 18:45 < jrand0m> 굿 18:45 <@nop> 지금은 업무 중이라 바쁘대요 18:46 < jrand0m> 좋아요 18:46 <@hezekiah> 마지막으로: C API에서는, Java에서 'interface'가 되는 	구조체에 대해 각 함수가 아마 그 구조체에 대한 구조체 포인터를 받을 거예요. 18:46 <@nop> hezekiah: 좋아 보입니다 18:46 <@nop> 좋아 보이네요 18:46 <@hezekiah> I2PSession       createSession(String keyFileToLoadFrom, 	Properties options); 18:46 <@hezekiah>  would be: 18:46 <@nop> 자바의 비-네이티브 데이터 타입들이란 게 18:46 <@hezekiah> I2PSession* createSession(I2PClient* client, char* 	keyFileToLoadFrom, Properties* options); 18:46 <@nop> ;) 18:46 < jrand0m> 헤헤 18:46 < jrand0m> 맞아요 hezekiah 18:47 < jeremiah> 유니코드는 다루나요? 18:47 <@hezekiah> 어쨌든 그 차이들을 감수할 수 있다면, 그 밖의 부분에서 	C와 Java API는 동일해야 해요. 18:47 <@hezekiah> nop? 유니코드요? :) 18:47 < jrand0m> UTF8, 아니면 UTF16 18:48 <@hezekiah> 아마 유니코드는 애플리케이션 레벨에서 	처리해야 할 거예요. 18:48 < jrand0m> 맞아요, 문자셋은 전적으로 메시지 내용의 문제죠 18:48 <@hezekiah> 아하. 18:48 < jeremiah> 오케이 18:48 <@hezekiah> Java String은 유니코드로 처리되죠, 그렇죠 jrand0m? 18:48 < jrand0m> bitbucket은 전부 비트 단위로 정의될 거예요 18:48 < jrand0m> 네 hezekiah 18:48 < jrand0m> (명시적으로 문자셋 변경을 지시하지 않는 한) 18:49 <@hezekiah> 그러니까 C API가 문자열을 유니코드로 구현하지 않는 한, 	Java API로 보낸 문자열과 C API로 보낸 문자열은 달라질 거예요. 18:49 < jrand0m> 관련 없어요 18:49 <@hezekiah> 알겠습니다. 18:49 < jrand0m> (app->API != API->router.  we only define API->router) 18:49 <@hezekiah> 제가 말하려는 건 이거예요, jrand0m: 18:50 <@hezekiah> 제가 Java API로 비밀번호를 설정하면, 그건 router를 통해 	어딘가 밖으로 나가죠. 18:50 < jrand0m> 비밀번호요? Destination을 만든다는 뜻인가요? 18:50 <@hezekiah> 그다음 다른 router를 찾아서, 그걸 C로 구현된 	다른 API(?)로 보내죠. 18:50 <@hezekiah>   void            setPassphrase(String old, String new); 18:50 <@hezekiah> 그 함수요. 18:51 < jrand0m> hezekiah> 그건 router의 관리용 메서드에 접근하기 위한 	관리자 비밀번호예요 18:51 <@hezekiah> 아 18:51 <@hezekiah> Java String을 쓰는 API 함수 중에, 그 String이 다른 API로 	전송되는 경우가 있나요? 18:51 < jrand0m> 앱의 99.9%는 I2PSession만 쓰고 	I2PAdminSession은 쓰지 않을 거예요 18:51 <@nop> 또한, router를 통해 운반되는 건 전부 네트워크 전송용으로 	변환되죠, 맞죠? 18:51 <@hezekiah> 그렇다면 유니코드를 쓰는 게 좋겠네요. 18:51 <@nop> 유니코드는 관련 없어요 18:52 < jrand0m> hezekiah> 아니요. 라우터 간 정보는 모두 	bit bucket으로 정의될 거예요 18:52 <@hezekiah> 알겠습니다. 18:52 < jrand0m> 맞아요 nop, 트랜스포트 레벨에서요 18:52 <@hezekiah> (bit bucket이 그냥 바이너리 버퍼라는 뜻이죠?) 18:53 < jrand0m> bit bucket은 첫 번째 비트는 X, 두 번째 비트는 Y, 	3~42번째 비트는 Z를 의미한다는 식의 정의를 말해요 18:53 < jrand0m> (예: 인증서 bitbucket에는 X.509를 쓰고 싶을 수도 있죠)

18:53 <@hezekiah> 그건 전에 다뤄본 적이 없어요.
18:54 <@hezekiah> 도착해서 맞닥뜨리면 그때 걱정하죠. :)
18:54 < jrand0m> ㅎㅎ 그렇지
18:55 < jrand0m> 좋아, 오늘 다루려던 네 가지: *router 아키텍처, *성능 모델, *공격 분석, *psyc. 첫 번째는 끝냈고, thecrypto가 오프라인이라 이건 미루는 게 어떨까 (모델에 대한 생각이 있다면 모르겠지만, nop?)
18:57 <@hezekiah> 음... jrand0m. 질문이 하나 더 있어요.
18:57 < jeremiah> jrand0m: 네트워크 스펙 최신 버전은 어디 있어요? 13일에 보낸 그거 맞나요?
18:57 < jrand0m> 예, 선생님?
18:57 <@hezekiah> 음, router 아키텍처에서는 API가 Application에서 /보내 오는/ 키를 처리하게 되어 있어요.
18:57 < jrand0m> jeremiah> 네
18:57 <@nop> 지금은 없네요
18:58 <@hezekiah> 그러니까... API가 키를 받는 유일한 방법은 createSession에서인 것 같아요.
18:58 < jrand0m> hezekiah> router는 공개키와 서명을 받을 뿐, 개인키는 받지 않아요
18:58 < jrand0m> 맞아요
18:58 <@hezekiah> 하지만 그건 파일이 필요하죠.
18:58 < jrand0m> 키는 파일이나 API의 메모리에 저장돼요
18:58 < jrand0m> 네
18:58 <@hezekiah> 그런데 애플리케이션이 키를 생성한다면, 그냥 버퍼로 API에 보내면 안 되나요?
18:59 <@hezekiah> 꼭 파일에 저장한 다음에 파일 이름을 넘겨야 하나요?
18:59 < jrand0m> 아니요, 원하시면 메모리에 둘 수 있어요
18:59 <@hezekiah> 그런데 API에는 그걸 할 수 있는 기능이 없잖아요.
18:59 <@hezekiah> 그냥 생각해본 거예요.
19:00 <@hezekiah> 키를 한 번만 생성하고 여러 번, 아주 많이 사용한다면(GPG 키처럼) 파일이 타당하죠.
19:00 -!- mihi [none@anon.iip] 님이 퇴장했습니다 [다들 잘 있어요, 늦어지고 있네요...]
19:00 <@hezekiah> 하지만 더 자주 생성될 거라면, 어떤 구조체나 버퍼 같은 걸로 API에 직접 보내는 방법이 있으면 좋겠어요
19:00 <@hezekiah> .
19:01 < jrand0m> 맞아요, 한 번, 딱 한 번만 생성돼요(알루미늄 모자 쓴 사람처럼 편집증이 아니라면)
19:02 < jrand0m> 다만 createDestination(keyFileToSaveTo)가 그 키를 생성할 수 있게 해줘요
19:02 <@hezekiah> 좋아요.
19:02 <@hezekiah> 그러면 App에서 API로 직접 전달할 필요는 없겠네요. 파일이면 충분하죠.
19:03 <@hezekiah> 제가 무례하게 끼어들기 전에 어디까지 얘기했죠? :)
19:06 < jeremiah> 그러면 지금은 client용이 아니라 router API만 작업 중인 거죠?
19:06 < jrand0m> 음, 지금은 성능 분석은 건너뛰죠(다음 주 전에 메일링 리스트에서 관련 논의가 좀 있으면 좋겠네요?). 그리고 공격 분석도 아마 마찬가지일 거예요(새 스펙을 읽고 코멘트가 있는 사람이 없다면요)
19:07 <@hezekiah> 그걸 건너뛰면, 지금은 뭘 얘기해야 하죠?
19:07 <@hezekiah> psyc?
19:07 < jrand0m> 다른 코멘트 가져온 사람 없으면...?
19:08 <@hezekiah> 음, 이번만은 내 코멘트 구멍(일명 악명 높은 내 입)이 비었네요.
19:08 < jrand0m> ㅎㅎ
19:09 < jrand0m> 좋아요, IRC 쪽이 어떻게 동작할지, 그리고 psyc이 관련 있거나 유용할지에 대한 생각 있는 분?
19:09 < jeremiah> 여담(좀 열받던데): wired의 "Wired, Tired, Expired" 목록에서 Waste를 'wired'로 분류했더라고요
19:09 < jrand0m> 헐
19:09 < jrand0m> 우리가 사람들 얼마나 깜짝 놀라게 할지 실감하나요?
19:09 < jeremiah> 그럼요
19:09 <@hezekiah> jrand0m: 그건 우리가 이걸 작동시키는 데 성공한다는 전제죠.
19:10 < jrand0m> 작동할 거라고 장담해요.
19:10 <@hezekiah> 세상엔 실패한 시도들이 많죠.
19:10 < jrand0m> 이거 하려고 직장도 그만뒀어요.
19:10 <@hezekiah> 그럼 진짜 모두를 놀라게 하겠네요. :)
19:10 <@hezekiah> 그런데요. 그러고도 밥벌이는 어떻게 하죠?
19:10 <@hezekiah> GPL 코드로는 돈이 잘 안 되거든요. ;-)
19:10 < jrand0m> 흐흐
19:11 <@hezekiah> psyc에 관해서는... 이렇게 말해볼게요:
19:11 <@hezekiah> 내가 처음 들은 때는, 그 얘기를 우리에게 이메일로 보냈을 때였어요.
19:11 < jrand0m> 젠장, 그거 내가 찾은 게 아닌데요 :)
19:11 <@hezekiah> 하지만 IRC는 아마도(아니면 /가장/) 널리 쓰이는 채팅 프로토콜 중 하나예요.
19:11 <@hezekiah> 사람들은 psyc이 무엇인지 /알기도/ 훨씬 전에 IRC 앱을 원할 거예요.
19:11 <@hezekiah> jrand0m: 이런. 미안. 그건 잊고 있었네요. :)
19:12 < jrand0m> psyc 쪽 말로는 아니래요. 역사가 아마 86년까지 거슬러 올라간다네요
19:12 <@hezekiah> 요점은 프로토콜의 우월함보다, 누가 쓰느냐가 더 중요하다는 거예요.
19:12 <@hezekiah> 그들의 _역사_는 그렇게 오래됐을지 몰라요.
19:12 <@hezekiah> 하지만 실제로 Psyc을 _쓰는_ 사람이 얼마나 되죠?
19:12 < jeremiah> 그러게요, 제가 태어난 지 1년 뒤부터 있었다면(에헴) 아직 그리 크지 않은 거네요
19:12 <@hezekiah> 제 말은, 그게 더 나은 프로토콜이라 해도 대부분은 IRC를 _쓴다_는 거예요.
19:13 <@hezekiah> 우리가 세상에서 가장 뛰어난 I2P 네트워크를 만들 수도 있지만...
19:13 -!- Ehud [logger@anon.iip] 님이 퇴장했습니다 [핑 타임아웃]
19:14 < jeremiah> 우리가 왜 이걸 신경 쓰는지 간단히 설명해 줄 사람? IRC는 가능한 애플리케이션 중 하나일 뿐이고, 원한다면 네트워크가 psyc도 유연하게 지원할 수 있다고 생각했는데요
19:14 <@hezekiah> 맞아요.
19:14 <@hezekiah> psyc도 만들 수는 있어요...
19:14 <@hezekiah> ... 하지만 더 많은 사람이 쓰니까 IRC부터 하자고 말하는 거예요.

19:14 <@hezekiah> jrand0m, 우리가 훌륭한 I2P 네트워크를 만들 수는 있지만, 사람들이 원하는 게 담겨 있지 않으면 	사람들은 쓰지 않을 거야.
19:14 < jrand0m> jeremiah> psyc가 흥미로운 이유는 우리가 	psyc가 작동하는 것과 같은 맥락으로 IRC를 구현하고 싶을 수도 있기 때문이야
19:15 <@hezekiah> 그러니 그들에게 '킬러 앱'을 제공해야 해.
19:15 < jeremiah> 오케이
19:15 < jrand0m> 맞아, IIP는 보이지 않는 IRC 프로젝트고, 사람들이 	IRC를 돌릴 수 있게 해줄 거야
19:16 < jrand0m> 중앙 서버 없이(사실상 어떤 서버도 없이), 	IRC가 어떻게 동작할지 알아내려면 고민할 게 많아. 	psyc에는 그에 대한 가능한 해답이 있어
19:16 < jrand0m> 물론 다른 방법들도 있고
19:17 <@hezekiah> 말했듯이 psyc가 더 나을 수도 있지만, 사람들이 IRC를 쓰고 싶어하지, 	psyc는 아니야.
19:17 < jrand0m> 그렇게 될 거야
19:17 < jrand0m> 사람들은 IRC를 쓸 거야
19:17 <@hezekiah> 결국 마케팅이 전부야, 베이비! ;-)
19:17 < jeremiah> 오늘 밤에 스펙이랑 psyc 관련 자료 좀 읽어볼게
19:17 < jrand0m> 좋지
19:17 <@hezekiah> ㅋㅋ
19:17 < jeremiah> 내일 5:00 UTC에 만날 계획 어때?
19:17 <@hezekiah> 글쎄?
19:18 < jeremiah> 아니면 아무 때나
19:18 < jrand0m> 난 iip에 24x7 접속해 있어 :)
19:18 < jeremiah> 응, 근데 난 밥은 먹어야지
19:18 <@hezekiah> jrand0m: 알아챘어.
19:18 < jrand0m> 05:00 utc 아니면 17:00 utc?
19:18 <@hezekiah> jeremiah: ㅋㅋ!
19:18 <@hezekiah> 음, iip-dev 회의는 공식적으로 21:00 UTC에 시작해.
19:18 -!- Ehud [~logger@anon.iip]님이 #iip-dev에 입장했습니다
19:19 < jeremiah> 오케이, 05:00 UTC라고 한 건 그냥 아무 생각 없이 헛소리한 거야
19:19 < jeremiah> mids는 어디 갔어?
19:19 <@hezekiah> mids는 잠시 프로젝트를 떠났어.
19:19 <@hezekiah> 몇 번 전 회의에 너도 있었잖아, 아니었어?
19:19 < jeremiah> 오케이
19:19 < jeremiah> 아닌가 보네
19:19 <@hezekiah> 의제의 일부로 일종의 송별회를 했어.
19:19 < jeremiah> 아
19:20 <@hezekiah> 좋아 ...
19:20 <@hezekiah> 아직 의제에 남은 게 있나?
19:20  * jrand0m 내 쪽에는 남은 게 없어
19:20 < jeremiah> psyc 관련:
19:20 < jeremiah> 이게 psyc의 기능이라면, 네가 	얼마 전에 언급했던 걸로 알아
19:20  * hezekiah 애초에 의제가 없었어 placve
19:21 <@hezekiah> pace
19:21 <@hezekiah> place
19:21 < jeremiah> 방 안의 각 사용자가 	다른 모든 사용자에게 메시지를 보내게 하는 건 현명한 생각은 아닌 것 같아
19:21 <@hezekiah> 됐다!
19:21 < jrand0m> jeremiah> 그럼 중복으로 지정된 pseudoservers가 	메시지를 재분배하도록 하겠다는 거야?
19:21 < jrand0m> (pseudoservers = 채널에서 사용자 목록을 가지고 있는 피어들)
19:21 < jeremiah> '브로드캐스팅'도 그다지 똑똑한 방식은 아닌 것 같은데, 그런데

모뎀을 쓰는 특정 사용자에게는 _엄청_ 많은 대역폭이 필요할 것 같고,	게다가 예를 들어... 20개의 메시지를 각각 따로 보내면서 생기는 지연 때문에	대화가 엉망이 될 거예요
19:21 < jeremiah> 최선의 해법은 모르겠지만, 아마 그게 하나의 방법일 수도 있겠죠
19:22 < jeremiah> 원한다면 직접 메시징이 좋을 것 같아요,	하지만 그게 아마 그리 중요하지 않은 경우들도 있어요
19:22 <@hezekiah> 메시지는 작성자의	개인 키로 서명되어야 진정성이 보장됩니다.
19:22 <@hezekiah> 이 문제는 당분간은 중요하지 않겠지만,	jeremiah 말에도 일리가 있다고 봐요
19:22 < jrand0m> hezekiah> 그건 사용자들이 증명 가능한 통신을 원해야 한다는 뜻이지 :)
19:23 < jrand0m> 맞아.
19:23 <@hezekiah> 채널에 있는 사용자 100명에게 내가 메시지를 보내야 한다면 ...
19:23 < jeremiah> 평균적으로 내 메시지는 수백 바이트 정도에 불과해서,	수백 명에게 보내도 그리 어렵진 않을지도 몰라
19:23 <@hezekiah> ... 음, 내 대화는 /아주/ 느려질 거야.
19:23 < jeremiah> 특히 응답을 기다리지 않는다면 더더욱
19:23 <@hezekiah> 한 메시지 보내는 데 20K.
19:23 <@hezekiah> 그건 아닌 듯. :)
19:23 < jrand0m> 글쎄, 채널에 100명이 있다면, *누군가*는	100개의 메시지를 내보내야 해
19:23 < jeremiah> 그게 20k야?
19:23 < jeremiah> 아, 맞다
19:23 <@hezekiah> 200명
19:24 < jeremiah> 흠
19:24 < jeremiah> 그런 건 routers가 잘하지 않을까?
19:24 < jeremiah> 대역폭이 그럭저럭 괜찮다고 어느 정도는 가정해도 될 것 같은데,	그치?
19:24 <@hezekiah> 각자 'router 구현'을 갖고 있다고 생각했는데
19:24 < jrand0m> 꼭 그렇진 않아.  릴레이가 있다면, 지명 메커니즘이	그걸 고려해야 해
19:24 < jrand0m> 그래, hezekiah
19:24 < jeremiah> 나는 스펙을 안 읽어봤어
19:25 < jrand0m> router는 네 로컬 router야
19:25 <@hezekiah> 으윽!
19:25 <@hezekiah> 아직도 너희 닉을 계속 헷갈려!
19:25 <@hezekiah> lol
19:25 < jrand0m> hehe
19:25 <@hezekiah> 음 ... nop은 어디 갔지?
19:25 <@hezekiah> 오.
19:26 <@hezekiah> 아직 여기 있네.
19:26 <@hezekiah> 잠깐 나간 줄 알았어,
19:26 < jrand0m> 하지만 jeremiah 말이 맞아, psyc에 우리가	검토해볼 만한 아이디어들이 있어, 물론 거부할 수도 있겠지만
19:26 <@hezekiah> 일단 네트워크부터 돌아가게 하자.
19:26  * jrand0m 그 말에 건배한다
19:26 <@hezekiah> 결승선만 바라보다 보면,	바로 3인치 앞의 돌부리에 걸려 넘어진다.
19:27  * jeremiah 영감이 솟는다
19:27 <@hezekiah> lol
19:27 < jrand0m> 다음 주까지 네트워크 스펙을 검토하는 걸 목표로 하면 정말 좋겠다고 생각해,	누구든 생각이나 코멘트가 있을 때마다 iip-dev로 이메일을 보내고.   내가 미친 걸까?
19:27 <@hezekiah> nop? 안건에 더 추가할 게 있나요,	아니면 여기서 산회할까요?
19:27 <@hezekiah> jrand0m: 음, 그걸 전부	다음 주까지 읽을 수 있을지는 모르겠지만, 노력은 해볼게요. :)
19:27 < jrand0m> 헤헷
19:28 < jrand0m> 그거 지독한 15페이지지 ;)
19:28 <@hezekiah> 15페이지?
19:28 <@hezekiah> 120페이지쯤으로 보이던데!
19:29 < jrand0m> 헤헷, 글쎄, 화면 해상도에 따라 다르겠지 ;)
19:29 < jeremiah> 거기에 앵커가 엄청 많아서	엄청 커 보이는 거야
19:29 < jrand0m> 헤헤
19:29 <@hezekiah> 왼쪽엔 링크가 15개보다 훨씬 더 많던데, 친구!
19:29 <@hezekiah> 실토해!
19:29 <@hezekiah> 15개보다 많잖아. :)
19:29 <@hezekiah> 오!
19:29 <@hezekiah> 그건 페이지가 아니네! 그냥 앵커들이잖아!
19:29 <@hezekiah> 살았다!
19:30  * hezekiah 익사 직전에 구출된 선원이 된 기분
19:30 < jeremiah> 수업, 4권 2장 메시지 바이트 구조로 넘어갑니다
19:30 < jrand0m> lol
19:30 <@hezekiah> lol
19:30 <@nop> 산회
19:30 <@hezekiah> *baf*!
19:30 <@hezekiah> 다음 주, 21:00 UTC, 같은 곳에서.
19:30 <@hezekiah> 그때 다들 봐요. :)
19:30 < jeremiah> 또 봐 --- 로그 종료 Tue Jul 15 19:30:51 2003 </div>
