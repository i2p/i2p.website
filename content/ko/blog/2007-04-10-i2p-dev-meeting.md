---
title: "I2P Dev Meeting - April 10, 2007"
date: 2007-04-10
author: "jrandom"
description: "2007년 4월 10일자 I2P 개발 회의 기록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> Complication, jadeSerpent, jrandom, mrflibble</p>

## 회의 기록

<div class="irc-log"> 16:01 &lt;jrandom&gt; 0) 안녕하세요 16:01 &lt;jrandom&gt; 1) 네트워크 상태 16:01 &lt;jrandom&gt; 2) Syndie 개발 상태 16:01 &lt;jrandom&gt; 3) ??? 16:01 &lt;jrandom&gt; 0) 안녕하세요 16:01  * jrandom 손을 흔든다 16:01 &lt;jrandom&gt; 간단한 주간 상태 노트는 http://dev.i2p.net/pipermail/i2p/2007-April/001343.html 에 올려두었습니다 16:01  * mrflibble 손을 흔들어 답한다 16:03 &lt;jrandom&gt; 그 노트가 충분히 짧으니, 1) 네트워크 상태부터 바로 들어가죠 16:03 &lt;jrandom&gt; 최근에는 꽤 잘 돌아가는 것 같습니다 16:03 &lt;jrandom&gt; 현재로서는 네트워크에 진행 중인 큰 변경 사항은 없어서(제가 아는 한), 당분간 그 상태가 유지될 듯합니다 16:03 &lt;jadeSerpent&gt; IRC도 드디어 잠잠해진 것 같네요 16:03 &lt;jrandom&gt; 좋네요 16:05 &lt;jrandom&gt; 1) 네트워크 상태에 덧붙일 내용은 많지 않습니다. 다른 분이 없으시면 2) Syndie 개발 상태로 넘어가죠 16:07 &lt;jrandom&gt; 다음 리비전이 예상보다 오래 걸리고 있지만, 2~3일 안에 새 릴리스를 내보내려고 합니다 16:07 &lt;jrandom&gt; 데스크톱 GUI는 아니겠지만, 여러 개선 사항이 포함될 것입니다 16:08 &lt;Complication&gt; 배포 안정성에 도움이 되는 거라면 뭐든 훌륭하죠 16:08 &lt;Complication&gt; 요즘 비교적 좋지 않았거든요 16:08 &lt;jrandom&gt; 네, 그 문제는 (어느 정도는) 비교적 쉽게 정리할 수 있을 겁니다 16:09 &lt;jadeSerpent&gt; i2p를 통한 가져오기 실패의 원인이 뭔지 아시나요? 16:09 &lt;jrandom&gt; 네, 타임아웃이 너무 짧습니다 16:10 &lt;jrandom&gt; (그리고 서버의 핸들러 스레드 수가 적습니다) 16:13 &lt;jrandom&gt; 좋습니다, 2) Syndie 개발 상태에 더 없으면 3) ??? 로 넘어가죠 16:13 &lt;jrandom&gt; 회의에서 더 논의할 사항이 있을까요? 16:14  * mrflibble 손을 흔든다 16:14 &lt;mrflibble&gt; 미안,  항목 1으로  다시 돌아가자 16:15 &lt;mrflibble&gt; &lt;jadeSerpent&gt; IRC도 드디어 잠잠해진 것 같네요 - 특별한 이유가 있어서라고 보시나요? 16:16 &lt;jrandom&gt; IRC 서버에 네트워크와 하드웨어 문제가 좀 있었고, 대부분이 지금은 최신 릴리스로 업그레이드해서(zzz의 개선점 혜택을 보게 되었죠) 16:17 &lt;jrandom&gt; tunnel 생성 성공률에 대한 수치가 훨씬 좋아 보입니다 16:17 &lt;mrflibble&gt; 아, 그렇군요, 서버 자체 문제였군요 16:17 &lt;mrflibble&gt; zzz의 개선사항은 뭐였죠? 16:19 &lt;Complication&gt; 메시지 우선순위로, tunnel 트래픽보다 tunnel 빌드 메시지가 우선되도록 했고 16:19 &lt;Complication&gt; 그리고 streaming lib(스트리밍 라이브러리) 조정, 늘 그렇듯 I2PSnark 수정 모음도요 16:19 &lt;mrflibble&gt; 아,  고마워요 16:19 &lt;jrandom&gt; (Complication이 말한 그대로요 :) 16:22 &lt;jrandom&gt; 좋습니다, 회의에 더 논의할 사항 있나요? 16:26 &lt;jrandom&gt; 없다면 16:26  * jrandom 마무리한다 16:26  * jrandom *baf*s 회의를 닫는다 </div>
