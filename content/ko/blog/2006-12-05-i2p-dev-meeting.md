---
title: "I2P 개발자 회의 - 2006년 12월 5일"
date: 2006-12-05
author: "jrandom"
description: "2006년 12월 5일자 I2P 개발 회의 기록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> burl, Ch0Hag, jrandom</p>

## 회의 기록

<div class="irc-log"> 15:00 &lt;jrandom&gt; 0) 안녕하세요 15:00 &lt;jrandom&gt; 1) 네트워크 상태 15:00 &lt;jrandom&gt; 2) Syndie 개발 현황 15:00 &lt;jrandom&gt; 3) iToopie 15:00 &lt;jrandom&gt; 4) ??? 15:00 &lt;jrandom&gt; 0) 안녕하세요 15:00  * jrandom 손을 흔든다 15:00 &lt;jrandom&gt; 주간 상태 노트를 http://dev.i2p.net/pipermail/i2p/2006-December/001321.html 에 올려두었습니다 15:01 &lt;jrandom&gt; (회의 2시간 전쯤에요! :) 15:01 &lt;jrandom&gt; 좋아요, 1) 네트워크 상태부터 들어가죠 15:01 &lt;jrandom&gt; 전체적으로 꽤 잘 되고 있고, 이 부분에서는 큰 변화가 없습니다 15:02  * jrandom 여기 irc에 벌써 20일째 연결되어 있네요 (아마 기록일 듯) 15:03 &lt;jrandom&gt; 지금으로서는 이 부분에 덧붙일 게 그다지 없네요 15:03 &lt;jrandom&gt; 그래서, 더 없으면 2) Syndie 개발 현황으로 넘어가죠 15:04 &lt;jrandom&gt; 여기서는 진전이 계속되고 있고, 자잘한 부분들이 더 작동 가능해지고 있습니다 15:04 &lt;jrandom&gt; 그래도 아직 꽤 거칠어요... "기능주의적", 그래픽도 기능주의적 ;) 15:05 &lt;jrandom&gt; 알파가 당장 임박한 건 아니지만, 곧 준비되길 바랍니다 15:07 &lt;jrandom&gt; 아무튼, 추가 정보가 나오면 알려드릴게요 :) 15:08 &lt;jrandom&gt; 좋아요, 잠깐 3) iToopie로 넘어가죠 15:08 &lt;jrandom&gt; 노트에 언급했듯이, 모두 고마워요!  :) 15:08 &lt;jrandom&gt; 좋아요, 속전속결로 4) ???로 계속하죠 15:08 &lt;jrandom&gt; 회의에서 제기하고 싶은 내용 있으신가요? 15:10 &lt;jrandom&gt; (마지막 10분 회의 이후 아마 1~2년쯤 됐을 텐데, 어쩌면 그게 더 좋았을지도요) 15:10 &lt;+fox&gt; &lt;Ch0Hag&gt; 어이쿠 와. 완전 우연히 I2P 회의에 실제로 참석했네. 15:11 &lt;+fox&gt; &lt;Ch0Hag&gt; 엄마, 안녕! 15:11 &lt;+fox&gt; &lt;Ch0Hag&gt; 이거 로그에 남는 거 맞지? :) 15:11 &lt;jrandom&gt; 헤헷 맞아 ch0 ;) 15:12 &lt;+fox&gt; &lt;Ch0Hag&gt; 왜냐면 우리 엄마가 I2P 회의 로그를 읽으시거든... 15:12 &lt;burl&gt; 라이선스에 관해 물어보려 했는데 www.i2p에서 방금 답을 읽었어요(왜 gpl이 아닌가요?) 15:13 &lt;jrandom&gt; gpl은 아기들을 죽입니다 15:13  * jrandom 몸을 숙인다 15:13 &lt;burl&gt; 엄마 드리려고 출력해야 해요. 컴퓨터를 잘 못하시거든요 15:13 &lt;jrandom&gt; 헤헤 15:14 &lt;burl&gt; 최근 자유 소프트웨어 운동에 대해 이것저것 읽고 있어요. 윤리적으로 딱 맞는 것 같아요 15:14 &lt;burl&gt; 폐쇄 소스는 악이에요 :) 15:14 &lt;jrandom&gt; 선이든 악이든 다 똑같죠.  여기서 중요한 건 폐쇄 소스는 /안전하지 않다/ ;) 15:15 &lt;jrandom&gt; (Syndie 라이선스 요약 @ http://syndie.i2p.net/faq.html#license i2p용 종교색이 덜한 라이선스 정보 @ http://www.i2p.net/licenses ) 15:15 &lt;burl&gt; 네, 그 생각도 스치긴 했어요. 어떤 사악한 회사가 Syndie를 훔쳐서 "더 나은" 폐쇄 버전을 만든다면 누가 그걸 믿겠어요? 15:16 &lt;jrandom&gt; 자유로운 것을 훔칠 수는 없죠 15:16 &lt;burl&gt; 네, 하지만 소스에 변경을 가하고는 보여주지 않는다는 얘기죠 15:17 &lt;jrandom&gt; 그건 소스의 /당신 사본/에 대한 변경이죠.  내 소스 사본은 여전히 예전 그대로이고, 여전히 똑같이 자유롭거든요 ;) 15:17 &lt;jrandom&gt; 하지만, 네, 이해해요.  동의하진 않지만 이해합니다 15:18 &lt;jrandom&gt; 모든 걸 고려하면, 오픈 소스&gt;&gt;폐쇄 소스이고, gpl에 불쾌한 제한이 좀 있더라도 많은 용도에 충분하고, 보안 측면에서도 충분히 개방적입니다 15:18 &lt;burl&gt; 아무도 그 폐쇄 버전을 신뢰하지 않을 테니, 인기에서 대체하진 못할 거예요 15:20 &lt;jrandom&gt; 그래요 15:21 &lt;jrandom&gt; 라이선스 투정은 회의 로그 10분을 채우는 데 언제나 좋은 방법이죠 ;) 15:21 &lt;jrandom&gt; 좋아요, 회의에 더 이야기할 거 있으신가요? 15:23 &lt;+fox&gt; &lt;Ch0Hag&gt; 음, 회의 시간을 더 채워야 한다면 - 왜 Java죠? 15:23 &lt;+fox&gt; &lt;Ch0Hag&gt; 그러니까, 으엑! 15:23 &lt;jrandom&gt; !thwap 15:24  * jrandom 준비 동작을 취한다 15:24  * jrandom *baf*s 하며 회의를 종료한다 </div>
