---
title: "I2P 개발자 회의 - 2006년 5월 2일"
date: 2006-05-02
author: "jrandom"
description: "2006년 5월 2일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단 정리

<p class="attendees-inline"><strong>참석자:</strong> green, jrandom</p>

## 회의 기록

<div class="irc-log"> 16:09 &lt;jrandom&gt; 0) 안녕하세요 16:09 &lt;jrandom&gt; 1) 네트워크 상태 16:09 &lt;jrandom&gt; 2) Syndie 상태 16:09 &lt;jrandom&gt; 3) ??? 16:09 &lt;jrandom&gt; 0) 안녕하세요 16:09  * jrandom 손을 흔든다 16:10 &lt;jrandom&gt; 주간 상태 노트를 http://dev.i2p.net/pipermail/i2p/2006-May/001285.html 에 게시했습니다 16:11 &lt;jrandom&gt; 좋습니다, 다들 그 흥미진진한 메일을 읽는 동안, 1) 네트워크 상태로 들어가 봅시다 16:13 &lt;jrandom&gt; 지금까지는 전체적인 혼잡 붕괴 문제는 해결된 것으로 보이고, tunnel 생성률도 꽤 좋습니다.  그래도 정리해야 할 이슈가 남아 있습니다 16:14 &lt;jrandom&gt; 이전에 논의했던 주기적 동작(보통 10~12분 간격으로 발생)이 여전히 존재해, 거부가 반비례적으로 발생합니다.  하지만 -1 시점의 새로운 코드 수정으로 그 문제는 없어질 것입니다 16:15 &lt;jrandom&gt; (즉, 이전의 망가진 무작위화와 달리 tunnel 만료 시간을 /제대로/ 무작위화합니다) 16:16 &lt;jrandom&gt; 그것과, 개선된 ssu 및 tunnel 테스트 스케줄링이 도움이 될 것이지만, 어느 정도일지는 아직 확신하지 못합니다 16:17 &lt;jrandom&gt; 좋습니다, 현재로서는 그 정도가 전부입니다.  1) 네트워크 상태에 대해 질문/코멘트/우려 사항 있으신가요? 16:18 &lt;green&gt; 흠, 최대 대역폭 제한에 전혀 도달하지 못하고 있고 이전과는 정말 많이 다릅니다 16:18 &lt;green&gt; 예를 들어 1-7에서처럼 16:18 &lt;green&gt; s/1-7/.12-7 16:18 &lt;jrandom&gt; 대역폭 공유 비율은 어떻게 설정되어 있나요?  이제 그건 매우 강력한 제어 수단입니다 16:19 &lt;green&gt; 80% 16:19 &lt;green&gt; 하지만 총 대역폭의 약 40%만 사용됩니다 16:20 &lt;green&gt; 이건 그냥 '아무것도 하지 않는 router'예요 :P 16:20 &lt;jrandom&gt; 흠, 대역폭이 80%까지 치솟는 일이 얼마나 자주 있나요? 그리고 tunnel 요청을 자주 거부하나요 (http://localhost:7657/oldstats.jsp#tunnel.reject.30 and tunnel.reject.*) 16:21 &lt;jrandom&gt; tunnel 요청의 주기성 때문에 실제로 과부하가 아닐 때도 종종 과부하로 감지되곤 합니다 16:21 &lt;jrandom&gt; (다른 때에는 router에 여유 용량이 있지만, 스파이크가 올 때는 그렇지 않기 때문이죠) 16:22 &lt;green&gt; tunnel.reject.30은 14 025,00건의 이벤트 동안 1,00처럼 매우 평평합니다 16:22 &lt;jrandom&gt; 아, 미안해요, 그 통계에서 핵심은 이벤트 건수 자체예요 - 대역폭 과부하 때문에 tunnel 요청을 14,000건 이상 거부했습니다 16:23 &lt;jrandom&gt; (그 통계의 "value"는 해당 이벤트에서 몇 개의 tunnel이 거부되었는지를 뜻하는데, 이벤트는 메시지로 인해 발생하므로 항상 1입니다) 16:27 &lt;jrandom&gt; 좋습니다, 1) 네트워크 상태에 대해 더 없으면, 2) Syndie 상태로 넘어가죠 16:27 &lt;jrandom&gt; Syndie 관련해 이메일에 있는 내용에 덧붙일 게 많지는 않고, 그냥 업데이트를 드리고 싶었습니다 16:28 &lt;jrandom&gt; 좋습니다, 그런 만큼 Syndie 관련해서 누군가 제기할 것이 없다면, 늘 하던 3) ???로 넘어가죠 16:28 &lt;jrandom&gt; 회의에서 더 다루고 싶은 내용이 있나요? 16:31  * tethra .17에 대해 (다시) "thanks"라고 말하고 싶어요, 정말 엄청난 개선이었거든요 16:33 &lt;jrandom&gt; 도움이 되어 기쁩니다, 그리고 더 많은 것들이 곧 나올 거예요 16:33 &lt;jrandom&gt; 좋습니다, 그런데 오늘 회의에 더 이상 내용이 없다면... 16:33  * jrandom 마무리한다 16:33  * jrandom *baf*s 회의를 종료한다 </div>
