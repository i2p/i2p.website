---
title: "I2P 개발자 회의, 2003년 8월 5일"
date: 2003-08-05
author: "nop"
description: "Java 개발 현황, 암호화 업데이트, 그리고 SDK 진행 상황을 다루는 제52차 I2P 개발자 회의"
categories: ["meeting"]
---

<h2 id="quick-recap">간단 요약</h2>

<p class="attendees-inline"><strong>참석자:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">회의 기록</h2>

<div class="irc-log"> <nop> 오케이, 회의 시작 <nop> 안건은 뭐죠 --> logger (logger@anon.iip) 가 #iip-dev에 참가했습니다 --> Anon02 (~anon@anon.iip) 가 #iip-dev에 참가했습니다 <hezekiah> Tue Aug  5 21:03:10 UTC 2003 <hezekiah> N번째 iip-dev 회의에 오신 것을 환영합니다. <hezekiah> 안건은 뭐죠? <thecrypto> Tue Aug  5 21:02:44 UTC 2003 <thecrypto> NTP stratum 2에 동기화됨 :) <hezekiah> Tue Aug  5 21:03:13 UTC 2003 --> ptm (~ptm@anon.iip) 가 #iip-dev에 참가했습니다 <hezekiah> 방금 NIST와 동기화했어요. :) <mihi> 이 동기화로 iip 지연이 줄어들진 않죠 ;) <jrand0m> nop: 다루고 싶은 것들: 자바 개발 상태, 자바 암호화 상태, 파이썬 개발 상태, sdk 상태, 네이밍 서비스 <hezekiah> (우리가 네이밍 서비스로 _벌써_ 들어가나요?) <jrand0m> 설계 얘기 말라는 거야, 이 바보야. 그건 co의 지껄임이잖아. 그냥 할 얘기 있으면 그거 얘기해. <hezekiah> 아 * jrand0m LART를 넣어둠 <jrand0m> 안건에 다른 거 더 있어? <jrand0m> 아니면 시작할까? <hezekiah> 음, 더 추가할 건 별로 떠오르지 않네요. <hezekiah> 아! <hezekiah> 오! <jrand0m> 오케이. 자바 개발 현황: <hezekiah> 좋습니다. <-- mrflibble 가 종료함 (핑 시간 초과) <nop> 오케이 <nop> 안건 <nop> 1) 환영 <jrand0m> 오늘 기준으로, 서로 통신할 수 있는 자바 클라이언트 API와 스텁 자바 router가 있습니다. 게다가 ATalk이라는 애플리케이션이 있어서 익명 IM + 파일 전송이 가능합니다. <nop> 2) IIP 1.1 블랙아웃 <nop> 3) I2P <nop> 4) 끝 - 코멘트와 기타 등등 * jrand0m 구석으로 돌아감 <nop> 미안    joeyo jrand0m Aug 05 17:08:24 * hezekiah가 jrand0m에게 구석에서 쓰라고 바보 모자를 건넴. ;-) <nop> 그건 미안 <nop> 거기서 시작한 줄 몰랐어 <nop> 나도 구석에 가야겠네 <hezekiah> ㅋㅋ <jrand0m> 걱정 마요. 항목 1) * hezekiah가 nop에게도 바보 모자를 건넴. :) <nop> 오케이 모두 환영합니다 <nop> 어쩌구 저쩌구 <nop> 2) IIP 1.1 블랙아웃 --> mrflibble (mrflibble@anon.iip) 가 #iip-dev에 참가했습니다 <hezekiah> 52번째 iip-dev 회의, 뭐 기타 좋은 헛소리까지! <nop> 서버가 최근 하드디스크 섹터 문제를 겪어서 교체했습니다 <nop> 그놈의 서버를 중복 구성을 갖춘 더 안정적인 환경으로 옮길 계획입니다 <nop> 그리고 여러 ircd 서버의 제어를 위임하는 방안도 검토 중 <nop> 글쎄 <nop> 그건 논의해 봐야겠죠 <-- Anon02 가 종료함 (클라이언트로부터 EOF) <nop> 하드드라이브를 교체했으니 이제 서버들이 계속 가동되길 바랍니다 <nop> 불편을 드려 죄송합니다 여러분 <nop> 3) I2P - Jrand0m, 진행해 주세요 <nop> 구석에서 나오세요 jrand0m * hezekiah가 구석으로 가서, jrand0m을 의자에서 끌어내리고, 연단으로 끌고 가서, 바보 모자를 빼앗고, 마이크를 건넴. * nop은 그 자리를 메우려고 그 구석으로 감 <hezekiah> ㅋㅋ! <jrand0m> 미안, 돌아왔어 * nop이 hezekiah에게서 바보 모자를 낚아챔 * nop이 자기 머리에 씀 * nop이 jrand0m에게 박수침 * jrand0m은 그냥 구경함 <jrand0m> 어... 음 오케이 <hezekiah> jrand0m: i2p, 자바 현황 등등. 말해봐요! <jrand0m> 그래서, 오늘 기준으로, 서로 통신할 수 있는 자바 클라이언트 API와 스텁 자바 router가 있습니다. 게다가 ATalk이라는 애플리케이션이 있어서 익명 IM + 파일 전송이 가능해요. <hezekiah> 파일 전송까지 벌써!? <jrand0m> 예, 맞아요 <hezekiah> 와. <hezekiah> 제가 한참 뒤처졌네요. <jrand0m> 다만 그렇게 매끈하진 않아요 <hezekiah> ㅋㅋ <jrand0m> 파일을 통째로 메시지 안에 던져 넣어요 <hezekiah> 이런. <nop> 1.8 mb 로컬 전송은 얼마나 걸렸어? <jrand0m> 4K 파일과 1.8Mb 파일로 테스트해봤어요 <jrand0m> 몇 초 <nop> 좋네 <nop> :) <hezekiah> 자바 쪽은 이제 진짜 암호화를 하나요, 아니면 아직도 가짜로 흉내만 내나요? <nop> 가짜 <nop> 그건 나도 알아 <nop> :) <jrand0m> 먼저 혼잣말로 예열했어요 [예: 한 창에서 다른 창으로 인사] 그래서 첫 elg의 오버헤드는 피했죠 <jrand0m> 맞아요, 대체로 가짜예요 <thecrypto> 암호화의 대부분은 가짜예요 <thecrypto> 그래도 그 부분은 작업 중이에요 <hezekiah> 물론이죠. :) <jrand0m> 확실히요. <jrand0m> 그와 관련해, thecrypto 업데이트 좀 해줄래요? <thecrypto> 음, 지금은 ElGamal과 SHA256을 끝냈어요 <thecrypto> 지금은 DSA용 소수 생성 작업 중이에요 <thecrypto> 5개를 보낼 테니 그중에서 하나 고르면 돼요 <hezekiah> nop: DSA에 쓸 소수를 가져오고 있지 않았나요? <thecrypto> ElGamal과 SHA256에 대한 벤치마크도 몇 가지 있어요 <thecrypto> 그리고 전부 빠릅니다 <jrand0m> elg 관련 최신 벤치마크: <jrand0m> 키 생성 시간 평균: 4437 총계: 443759 최소: 872    최대: 21110    초당 키 생성: 0 <jrand0m> 암호화 시간 평균    : 356 총계: 35657 최소: 431    최대: 611    암호화 Bps: 179 <jrand0m> 복호화 시간 평균    : 983 총계: 98347 최소: 881    최대: 2143    복호화 Bps: 65

<hezekiah>	min과 max: 초 단위인가요?
<jrand0m>	Bps는 실제로 큰 의미가 없다는 점에 유의하세요, 우리는 암호화/복호화 	  64바이트만 합니다
<thecrypto>	ms
<jrand0m>	아니요, 미안, 전부 밀리초입니다
<hezekiah>	좋네요. :)
<hezekiah>	그리고 이건 java로 하나요?
<thecrypto>	네
<thecrypto>	순수 java
<hezekiah>	OK. 정말 감명받았습니다. :)
<jrand0m>	100%.  P4 1.8
<thecrypto>	제 800 MHz에서도 거의 비슷합니다
<hezekiah>	저도 동일한 테스트를 하려면 어떻게 하나요?
<jrand0m>	sha256 벤치마크:
<jrand0m>	짧은 메시지 시간 평균  : 0 total: 0	min: 0	max: 	  0  Bps: NaN
<jrand0m>	중간 메시지 시간 평균 : 1 total: 130	min: 0	max: 	  10 Bps: 7876923
<jrand0m>	긴 메시지 시간 평균   : 146	total: 14641	min: 	  130	   max: 270	   Bps: 83037
<thecrypto>	ElGamalBench 프로그램을 실행하세요
<hezekiah>	OK.
<hezekiah>	찾아볼게요.
<jrand0m>	(짧은 길이: ~10바이트, 중간 ~10KB, 긴 ~ 1MB)
<jrand0m>	java -cp i2p.jar ElGamalBench
<jrand0m>	("ant all" 실행 후)
<hezekiah>	jrand0m: 감사합니다. :)
<jrand0m>	천만에요
<thecrypto>	NaN이라는 건 너무 빨라서 0으로 나누게 된다는 뜻이에요 	  그만큼 빠르다는 거죠 :)
<hezekiah>	sha 벤치마크는 뭐죠?
<jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip)님이 #iip-dev에 입장했습니다
<hezekiah>	OK.
<jrand0m>	아마 그것들을 관련 엔진들의 main() 메서드로 옮기고 싶을 텐데, 	  지금은 거기 있는 그대로도 괜찮아요
<hezekiah>	AMD K6-2 333MHz에서 이 모든 게 얼마나 빠른지 봅시다 (정수 연산으로는 	  그리 유명하지 않은 칩이거든요.)
<jrand0m>	ㅎㅎ
<jrand0m>	그러면 남은 건 DSA하고 AES죠?
<jrand0m>	정말 끝내줍니다, thecrypto.  멋진 작업이에요.
<thecrypto>	맞아요
<jrand0m>	나머지 둘의 ETA(예상 완료 시간)를 좀 알려줄 수 있을까요?  ;)
<hezekiah>	제 머신에서도 당신 것만큼만 빨라 준다면, 	  어떻게 그렇게 하는지 꼭 알려줘야 해요. ;-)
<thecrypto>	소수(primes)만 준비되면 DSA는 거의 바로 끝나요
<nop>	hezekiah python용 sslcrypto 써봤어
<thecrypto>	소수 생성기(prime generator)에서 코드 몇 개 가져오고 그런 	  것들만 하면 끝나요
<nop>	그 링크에 있는 그거
<hezekiah>	nop: sslcrypto는 우리에게 아무 도움이 안 돼요.
<hezekiah>	nop: 그건 ElGamal _or_ AES _or_ sha256를 구현하지 않아요.
<thecrypto>	AES는 거의 끝났는데 어딘가에 에러가 있어서 	  아직 찾아내서 제거하려는 중이고, 그거만 해결하면 끝나요
<jrand0m>	thecrypto> 그럼 금요일까지 DSA keygen, sign, verify, 그리고 임의 크기 입력에 대한 AES encrypt, 	  decrypt까지 되나요?
<nop>	McNab의 사이트에 있는 그건 아닌가?
<thecrypto>	그래요
<nop>	젠장
<thecrypto>	금요일쯤 될 거예요
<thecrypto>	아마 목요일이 더 유력해요
<jrand0m>	thecrypto> 거기에 UnsignedBigInteger 관련 것도 포함되나요?
<thecrypto>	여름 캠프 때문에 다음 주 회의는 못 나가고, 	  그 뒤에 돌아올게요
<thecrypto>	jrand0m: 아마 아닐 듯
<jrand0m>	ok.
<jrand0m>	그럼 당분간은 java와 python 사이의 상호운용성은 	  b0rked.
<jrand0m>	암호 쪽 얘기예요.
---	알림: jeremiah가 온라인입니다 (anon.iip).
-->	jeremiah (~chatzilla@anon.iip)님이 #iip-dev에 입장했습니다
<jrand0m>	(즉, 서명, 키, 암호화, 복호화용)

<nop>	흠, 아마 C/C++에 더 집중해야 할지도.
<thecrypto>	음, 완전히 동작하게 만들고 나면 java와 python이 서로 통신할 수 있게 확실히 할 수 있어	  .
<jrand0m>	네가 없는 동안 나는 unsigned 관련 사항을 살펴볼게.
<jeremiah>	누가 대화 기록을 이메일로 보내줄 수 있나요? jeremiah@kingprimate.com
<hezekiah>	jeremiah: 잠깐만요. :)
<jrand0m>	nop> C/C++ 개발자 있나요?
<nop>	한 명 있어, 응.
<nop>	그리고 Hezekiah도 할 수 있다는 걸 알고 있어.
<jrand0m>	아니면 hezekiah랑 	  jeremiah에게서 python 개발 진행 현황을 받아서 C/C++ 개발에 더 많은 사람이 합류할 때를 알아볼 수 있겠지.
<jrand0m>	맞아, 당연히.  그런데 hez+jeremiah는 지금 python 작업 중이지 	  (그치?)
<hezekiah>	응.
<--	mrflibble가 나갔습니다 (핑 타임아웃)
<hezekiah>	내가 불쌍한 jeremiah를 좀 많이 괴롭히고 있어요.
<nop>	내 말은, python이 속도가 빠르지 않을 거라면…
<hezekiah>	Python은 주로 내가 이 네트워크를 이해하려고 쓰는 거예요.
<nop>	아하
<hezekiah>	일단 기본적으로 전체 스펙을 따르게 만들면, 	  jeremiah에게 넘겨서 그의 판단대로 하게 할 생각이에요.
<hezekiah>	스펙을 최고 수준으로 구현하려는 건 아니어요.
<hezekiah>	(그게 목적이라면 C++를 쓸 거예요.)
<jeremiah>	음, 앱에서 진짜로 CPU를 많이 쓰는 부분은 	  내 기억이 맞다면(iirc) 암호화(crypto) 말고는 없고, 이상적으로는 그건 어차피 C에서 처리될 거잖아요, 그쵸?
<jrand0m>	그럼, jeremiah. 전부 앱에 달려 있어.
-->	mrflibble (mrflibble@anon.iip) 님이 #iip-dev에 입장했습니다
<hezekiah>	jeremiah: 이론적으로는.
<jrand0m>	그럼 python 쪽 진행은 어디까지야?  클라이언트 API, 로컬 전용 	  router, 등등?
<jeremiah>	python 구현은 처음부터 어떤 최적화를 할 수 있을지도 알려줄 거라서… 가능한 한 최신으로 유지하거나, 어쩌면 	  C 구현보다 앞서가게 만들고 싶어요.
<hezekiah>	jrand0m: 좋아요. 지금까지 한 건 이래요.
<hezekiah>	_이론상_으로는 router가 클라이언트에서 오는 관리자용이 아닌 	  모든 메시지를 처리할 수 있어야 해요.
<hezekiah>	하지만 아직 클라이언트가 없어서 디버깅을 못 했어요 	  (즉, 아직 버그가 있어요.)
<hezekiah>	지금 클라이언트를 작업 중이에요.
<jrand0m>	'k.  서명 검증을 비활성화할 수 있으면, 지금은 그걸 대상으로 	  java 클라이언트를 돌려볼 수 있을 거야
<hezekiah>	관리자 메시지를 제외하고는 그걸 하루 	  이틀 안에 끝내려고 해요.
<jrand0m>	미팅 끝나고 그걸 테스트해보자.
<hezekiah>	jrand0m: 좋아요.
<jeremiah>	지난 	  미팅 이후로는 주로 현실적인 일들을 처리하고 있었고, 클라이언트 API 작업은 할 수 있어요. 다만 제 생각을 hezekiah와 	  맞추려고 하고 있었어요
<jrand0m>	좋아
<hezekiah>	jeremiah: 있잖아요, 잠깐만 기다려요.
<hezekiah>	jeremiah: 지금 당장 처리하기엔 새걸 너무 많이 	  넣고 있는 것 같아요.
<jeremiah>	hezekiah: 맞아요. 제가 말하려던 건, 아마 기본적인 것부터 그냥 	  구현을 진행하는 게 좋겠다는 거였어요
<hezekiah>	jeremiah: 조금 지나면 안정화될 테니 그때 	  다듬기 시작하면 돼요. (도움이 필요한 TODO 코멘트가 많아요.)
<jeremiah>	그리고 전체 그림이 잡히면 나중에 제가 확장할 수 있어요
<hezekiah>	맞아요.
<hezekiah>	이 모든 코드를 당신이 유지보수하게 될 거예요. :)
<jrand0m>	좋아.  그럼 작동하는 python router + 클라이언트 API까지 eta 1~2주?
<hezekiah>	다음 주에 휴가를 가서 아마 그 정도요.
<hezekiah>	곧 router 간 상세한 내용이 더 나올까요?
<jrand0m>	아니.
<jrand0m>	음, 맞아.
<jrand0m>	하지만 아니.
<hezekiah>	ㅋㅋ
<jeremiah>	hezekiah: 휴가는 얼마나 길어요?
<hezekiah>	1주.
<jeremiah>	ok
<jrand0m>	(그러니까 SDK가 나가자마자, 내 시간의 100%는 I2NP로 들어간다는 뜻)
<hezekiah>	휴가 가기 전에 관리자용이 아닌 모든 기능을 	  작성해두려고 해요
<hezekiah>	.
<jrand0m>	그런데 돌아오고 나면 곧바로 대학 가는 거지, 맞지?
<hezekiah>	I2NP?
<hezekiah>	맞아요.
<jrand0m>	네트워크 프로토콜
<hezekiah>	휴가 끝나고 약 1주 정도 있어요.
<hezekiah>	그다음엔 떠나요.
<hezekiah>	그리고 제 여유 시간은 확 줄어요.
<jrand0m>	그러면 그 1주는 디버깅만 해야겠네
<jeremiah>	그래도 hez가 없는 동안 나는 코드를 작업할 수 있어요
<jrand0m>	오케이
<jrand0m>	jeremiah, 여름 일정은 어때?
<hezekiah>	jeremiah: 아마 그 admin 기능들을 동작하게 만들 수 있지 않을까요?

<thecrypto>	휴가에서 돌아오면 아직 한 달 정도는 이것저것 작업할 수 있을 거야 	  on things
<jrand0m>	인생을 사는 거야, 아니면 우리 나머지 l00ser들처럼 지내는 거야?  :)
<jeremiah>	아마도
<hezekiah>	100sers?
<hezekiah>	100ser가 뭐야?
<jeremiah>	난 22일에 대학으로 떠나, 그거 말곤 개발할 수 있어
<mihi>	hezekiah: 루저(loser)
<jeremiah>	그리고 떠나기 전 마지막 한 주에는 내 친구들이 전부 떠날 거라서... 그래서 	  하이퍼 개발 모드로 들어갈 수 있어
<hezekiah>	mihi: 아!
<jrand0m>	헤헤
<hezekiah>	좋아. 의제에서 우리가 어디까지 했지?
<hezekiah>	즉, 다음은 뭐지?
<jrand0m>	SDK 현황
<jrand0m>	SDK == 클라이언트 구현 하나, 로컬 전용 router 구현 하나, 앱 하나, 그리고 문서.
<jrand0m>	그걸 다음 화요일까지 내놓고 싶어.
<hezekiah>	jeremiah: 그 백로그는 가는 중이야. 거기서 너를 빼먹어서 미안. :)
<jeremiah>	고마워
<jrand0m>	좋아, co가 없으니, 네이밍 서비스 쪽 얘기는 아마 좀 시기상조일 거야
<jrand0m>	그가 스펙을 내놓거나 자리에 있을 때 네이밍 서비스에 대해 논의하자
<jrand0m>	좋아, I2P 얘기는 여기까지
<jrand0m>	다른 I2P 얘기 있는 사람? 아니면 다음으로 넘어갈까:
<nop>	4) 코멘트 등과 함께 마무리
<hezekiah>	딱히 떠오르는 게 없네.
<jrand0m>	다들 	  http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html 봤다고 생각해도 되지?
<thecrypto>	여기서는 아니야
<jrand0m>	(nop이 아까 여기 올렸어)
<hezekiah>	폭탄 제작 사이트로 링크했다가 체포된 그 사람 얘기?
<jrand0m>	응
<jrand0m>	가능한 한 빨리 I2P를 올려야 하는 이유와의 관련성은 분명할 거야 ;)
<hezekiah>	좋아! jeremiah, 그 로그들 지금 보냈어.
<jeremiah>	고마워
<jrand0m>	질문 / 코멘트 / 생각 / 프리스비 아무거나 있어? 	  아니면 기록적으로 짧은 미팅으로 끝낼까?
*	thecrypto 프리스비를 던진다 <--	logger가 퇴장함 (Ping timeout)
<jrand0m>	젠장 오늘 다들 엄청 조용하네 ;)
<mihi>	질문:
<mihi>	개발자가 아닌 사람은 어디서 너희 java 코드를 받을 수 있어?
<jrand0m>	si sr?
<thecrypto>	아직 아냐
<mihi>	404
<jrand0m>	릴리스 준비가 되면 공개할 거야.  즉, 소스는 SDK와 함께 나갈 거야
<jrand0m>	헤헷
<jrand0m>	그래, 우린 SF는 안 써
<hezekiah>	nop: 언젠가 anonymous cvs를 동작하게 할 수 있을까?
<hezekiah>	time?
<--	mrflibble가 퇴장함 (Ping timeout)
<nop>	음, 표준이 아닌 포트를 열어둘 거야
<jrand0m>	hezekiah> 코드에 GPL 라이선스를 붙이면 그걸 제공할 거야
<nop>	근데 나는 viewcvs 작업 중이야
<jrand0m>	즉, 아직은 아냐. gpl 문서가 코드에 아직 추가되지 않았거든
<hezekiah>	jrand0m: 그건 모든 python 코드 디렉터리와 모든 python 	  소스 파일에 있어, GPL-2 라이선스로 명시되어 있어.
<jrand0m>	hezekiah> 그게 cathedral에 있어?
<hezekiah>	응.
<jrand0m>	아 그렇군.  i2p/core/code/python ?  아니면 다른 모듈? *	jrand0m은 거기서 못 봤어
<hezekiah>	각 python 코드 디렉터리에는 	  GPL-2가 들어 있는 COPYING 파일이 있고, 각 소스 파일은 라이선스가 GPL-2로 설정되어 있어
<hezekiah>	그건 i2p/router/python 그리고 i2p/api/python 이야
<jrand0m>	'k
<jrand0m>	그래서, 다음 화요일까지는 SDK + 공개 소스 접근 권한을 제공할 거야.
<hezekiah>	좋네.
<hezekiah>	아니면 네가 좋아하는 표현대로, wikked. ;-)
<jrand0m>	헤헷
<jrand0m>	nada mas?
<hezekiah>	nada mas? 그게 무슨 뜻이야!?
<jeremiah>	더 없다는 뜻
*	jrand0m이 대학에서 스페인어 좀 배우라고 제안함 -->	mrflibble (mrflibble@anon.iip)가 #iip-dev에 입장함
<hezekiah>	질문 있나 누구?
<hezekiah>	한 번!
<--	ptm (~ptm@anon.iip)가 #iip-dev에서 나감 (ptm)
<hezekiah>	두 번!
<--	mrflibble가 퇴장함 (mr. flibble이 말하길 "game over boys")
<hezekiah>	지금 말하든가... 아니면 나중에 말하고 싶을 때 말하든가!
<thecrypto>	좋아, ElGamal을 더 최적화할 거니까, 앞으로 	  ElGamal 벤치가 더 빨라질 거라고 기대해
<jrand0m>	튜닝 전에 DSA와 AES에 먼저 집중해줘... 제발요오오오 :)
<thecrypto>	그럴게
<hezekiah>	그가 그걸 하는 이유는 내가 또 사람들한테 말썽을 부리고 있어서야. ;-)
<thecrypto>	난 DSA 소수(prime)를 만들고 있어
<--	mrflibble (mrflibble@anon.iip)가 #iip-dev에 입장함
<thecrypto>	음, 적어도 지금은 DSA 소수를 만드는 프로그램을 만들고 있어
<hezekiah>	Java의 ElGamal은 AMD K-6 II 333MHz를 좋아하지 않아.
<hezekiah>	좋아.
<hezekiah>	질문 시간 끝!
<jrand0m>	좋아 hez, 우리 끝났어.  java 클라이언트랑 python router 작업 	  맞춰보려고 잠깐 회의(powwow)할래?
<hezekiah>	여러분, 다음 주에 봐요 시민 여러분!
*	hezekiah가 *baf*er를 쾅 내리친다 </div>
