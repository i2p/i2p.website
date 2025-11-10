---
title: "I2P 개발자 회의 - 2005년 12월 13일"
date: 2005-12-13
author: "jrandom"
description: "2005년 12월 13일자 I2P 개발 회의 로그."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> cervantes, jrandom, spaetz</p>

## 회의 기록

<div class="irc-log"> 15:15 &lt;jrandom&gt; 0) 안녕하세요 15:15 &lt;jrandom&gt; 1) 네트워크 상태와 부하 테스트 15:15 &lt;jrandom&gt; 2) I2PSnark 15:15 &lt;jrandom&gt; 3) Syndie 15:15 &lt;jrandom&gt; 4) ??? 15:15 &lt;jrandom&gt; 0) 안녕하세요 15:15  * jrandom 손을 흔듭니다 15:15 &lt;jrandom&gt; 주간 상태 노트를 http://dev.i2p.net/pipermail/i2p/2005-December/001239.html 에 올렸습니다 15:15 &lt;jrandom&gt; (이번 주엔 회의 *전*에 - 누가 상상이나 했겠어요?) 15:16 &lt;jrandom&gt; 뭐, 어차피 다들 회의가 시작해야 읽으시니까요 ;) 15:16 &lt;jrandom&gt; 자, 그럼 1) 네트워크 상태와 부하 테스트로 넘어가죠 15:16 &lt;@cervantes&gt; 안녕하세요! 15:17 &lt;jrandom&gt; 자기 몫을 해줘서 고마워요, cervantes ;) 15:17 &lt;@cervantes&gt; 뭘 읽으라는 거죠? 15:17 -!- DreamTheaterFan [anonymous@irc2p] 님이 퇴장했습니다 [피어에 의해 연결이 리셋됨] 15:17 &lt;jrandom&gt; 메일에 쓴 것 외에 덧붙일 게 많진 않아요, 1)에 대해 질문이나 코멘트 있으신가요? 15:19 &lt;spaetz&gt; 부하 테스트는 실제 I2P 네트워크에서 하나요, 아니면 이를 위한 프라이빗 네트워크가 따로 있나요? 15:19 &lt;jrandom&gt; 라이브 네트워크에서 하고 있어요 15:19 &lt;spaetz&gt; 그냥 궁금해서요 15:19 &lt;spaetz&gt; ㅇㅋ 15:20 &lt;jrandom&gt; 다만 조심스럽게 진행 중입니다. 부하가 걸린 피어들에서는 과감히 물러서고, 물론 tunnel 거부도 준수합니다 15:20 &lt;@cervantes&gt; 최근 irc2p 불안정성은 테스트와 무관했습니다 15:21 &lt;@cervantes&gt; (궁금하셨을까 봐) 15:21 &lt;jrandom&gt; 새 설정은 잘 버티고 있나요, cervantes?   15:21 &lt;@cervantes&gt; 지금까지 아주 안정적이었습니다 15:22 &lt;jrandom&gt; 좋네요 15:22 &lt;@cervantes&gt; 문제의 원인을 추적하느라 좀 지루했을 뿐이죠 15:24 &lt;jrandom&gt; 좋아요, 다른 질문/코멘트가 없으면 2) I2PSnark로 넘어갈까요? 15:25 &lt;jrandom&gt; 넘어간 걸로 하죠 15:26 &lt;jrandom&gt; 자, 기본적으로 I2PSnark가 다시 잘 동작해야 합니다... BT 스펙에는 아직 없지만 azureus와 rufus가 사용하는 몇 가지 속성 때문에 호환성 문제가 있었는데, 제가 확인한 상황들에서는 이제 호환됩니다 15:26 &lt;jrandom&gt; 제가 테스트한 모든 토렌트에서 i2psnark가 이제 동작합니다만, 문제가 생기면 알려주세요 15:27 &lt;jrandom&gt; 그걸 고치려는 동기 중 일부는 몇 가지 SAM 버그와 관련이 있었고, I2PSnark은 SAM을 사용하지 않기 때문이기도 합니다 15:28 &lt;jrandom&gt; 그 부분에 더 덧붙일 건 별로 없네요... 질문이 없으시면 3) Syndie로 넘어가죠 15:29 -!- Xunk [Xunk@irc2p] 님이 퇴장했습니다 [피어에 의해 연결이 리셋됨] 15:30 &lt;jrandom&gt; 음, 그 부분도 메일에 쓴 것 이상의 내용은 별로 없어요 15:31 -!- Xunk [Xunk@irc2p] 님이 #i2p에 입장했습니다 15:31 &lt;jrandom&gt; Syndie 관련 질문이 없으시면 계속해서 4) ???로 자유 토론을 시작하죠 15:31 -!- DreamTheaterFan [anonymous@irc2p] 님이 #i2p에 입장했습니다 15:32  * jrandom 의제에 clunk 같은 게 없었다는 걸 기억합니다.  혹시 꺼내고 싶은 주제가 있나요? 15:32 &lt;@cervantes&gt; 이야 속도 빠르네 though 15:32 &lt;@cervantes&gt; *through 15:33 -!- bar [bar@irc2p] 님이 퇴장했습니다 [피어에 의해 연결이 리셋됨] 15:33 &lt;jrandom&gt; 그렇죠, 회의 로그에 글자만 보려고 말할 필요는 없죠 :) 15:33 -!- bar [bar@irc2p] 님이 #i2p에 입장했습니다 15:33 -!- mode/#i2p [+v bar] by chanserv 15:33 -!- mule [mule@irc2p] 님이 #i2p에 입장했습니다 15:35 &lt;jrandom&gt; 좋아요, 더 없으면... 15:35  * jrandom 몸을 풉니다 15:35  * jrandom *baf* 하며 회의를 종료합니다 </div>
