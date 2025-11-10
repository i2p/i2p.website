---
title: "I2P 개발자 회의 - 2006년 11월 28일"
date: 2006-11-28
author: "jrandom"
description: "2006년 11월 28일 I2P 개발 회의 기록."
categories: ["meeting"]
---

## 간단 요약

<p class="attendees-inline"><strong>참석자:</strong> gott, JosephLeBlanc, jrandom, zzz</p>

## 회의 기록

<div class="irc-log"> 15:14 &lt;jrandom&gt; 0) 안녕 15:14 &lt;jrandom&gt; 1) 네트워크 상태 15:14 &lt;jrandom&gt; 2) Syndie 개발 상태 15:14 &lt;jrandom&gt; 3) ??? 15:14 &lt;jrandom&gt; 0) 안녕 15:14  * jrandom 손을 흔든다 15:14 &lt;jrandom&gt; 주간 상태 노트를 http://dev.i2p.net/pipermail/i2p/2006-November/001320.html 에 올려두었습니다 15:14 &lt;jrandom&gt; (지연되어 죄송합니다, 부엌에서 작은 비상사태가 있었어요) 15:14 &lt;gott&gt; 안녕하세요, jrandom. 15:15 &lt;jrandom&gt; 안녕, gott 15:15 &lt;jrandom&gt; 좋아요, 1) 네트워크 상태로 들어가 봅시다 15:15  * jrandom 1) 네트워크 상태에 추가로 할 말은 없고, 다만 제가 IRC에 13일째 끊김 없이 접속 중이라는 점을 언급합니다) 15:16 &lt;gott&gt; i2psnark을 통해 #fr의 프랑스인들에게서 제가 좋아하는 모더니스트 영화 Metroland를 다운로드할 수 있었습니다 15:16 &lt;gott&gt; 다운로드 속도는 4400 kb/s; 업로드도 비슷합니다. 15:16 &lt;gott&gt; 피어 6개. 15:16 &lt;gott&gt; 유럽 모더니스트 픽션의 전파에 아주 좋네요. 15:16 &lt;jrandom&gt; !thwap 15:17 &lt;jrandom&gt; (혹시 실제로 4Mbps가 나오고 있다면, 양쪽 모두 0hop tunnel을 쓰고 있는 거죠) 15:17 &lt;gott&gt; 초당 바이트. 15:18 &lt;jrandom&gt; 1) 네트워크 상태에 대해 더 이야기할 것 있는 분? 15:20 &lt;jrandom&gt; 좋아요, 2) Syndie 개발 상태로 넘어가죠 15:20 &lt;gott&gt; 이 부분을 i2p에서 어떻게든 더 좋게 만들 수 있을까요? 15:20 &lt;jrandom&gt; gott: 아, kbps가 아니라 4400 Bps를 말한 거죠? 15:20 &lt;jrandom&gt; 그럼 0hop tunnel 얘기는 취소할게요 15:21 &lt;jrandom&gt; 현재 보통은 4KBps 정도이고, 더 나은 피어 선택과 혼잡 관리로 개선할 수 있습니다 15:22 &lt;jrandom&gt; 좋아요, Syndie 개발 상태는 메모에 적었듯이 많은 진전이 있습니다 15:23 &lt;jrandom&gt; 아직 메워야 할 빈틈이 좀 남았지만, 대체로 새 컴포넌트를 쓰는 게 아니라 빈틈을 메우는 작업입니다 15:24 &lt;jrandom&gt; 좋아요, 2) Syndie 개발 상태에 대해 더 있을까요? 15:25 &lt;jrandom&gt; 좋아요, 그럼 3) ??? 로 넘어가죠 15:26 &lt;jrandom&gt; 이 짧은 미팅에서 더 꺼낼 주제가 있을까요? 15:26 &lt;JosephLeBlanc&gt; 돈이 필요하세요? 15:26 &lt;JosephLeBlanc&gt; 아 젠장 15:26 &lt;JosephLeBlanc&gt; 그럼, 돈이 필요하신가요? 15:27 &lt;JosephLeBlanc&gt; 컴퓨터가 필요하세요? 15:27 &lt;JosephLeBlanc&gt; 맥주 원하세요? 15:27 &lt;JosephLeBlanc&gt; 뭐요? 15:27 &lt;jrandom&gt; 현재 재정은 꽤 괜찮은 편이고, 물론 후원은 언제나 감사히 받습니다 15:27 &lt;JosephLeBlanc&gt; 어서 말해봐요 15:27 &lt;JosephLeBlanc&gt; 좋아요, 그럼 15:27 &lt;+zzz&gt; emule 클라이언트에 현상금 걸어요 :) 15:28 &lt;jrandom&gt; (하지만 정말 돈이 주머니를 태울 정도로 급하시면, osx gui 테스트용으로 mac mini 하나 있으면 좋겠네요 ;) 15:28 &lt;jrandom&gt; ㅋㅋ zzz 15:28 &lt;JosephLeBlanc&gt; 모두가 갚아야 할 4만 달러의 학자금 대출을 가진 레즈비언 속물인 건 아니죠 15:28 &lt;+zzz&gt; 좋은 작업 계속하세요 jr 15:28 &lt;jrandom&gt; 그게 폐쇄형 제안이 아니었다면: 관심과 지원은 감사하지만, 앞으로 파일 공유 앱을 작업할 시간은 없을 거예요 15:29 &lt;JosephLeBlanc&gt; modulus의 lovesoc을 구현할 수 있나요 15:29 &lt;JosephLeBlanc&gt; ? 15:29 &lt;jrandom&gt; 고마워요 zzz, 당신도요 (당신의 서비스와 코드는 정말 큰 도움이 됩니다!) 15:29 &lt;+zzz&gt; baf 가져와요 ㅋㅋ 15:30  * jrandom 구석으로 달려간다 15:30  * jrandom 준비한다 15:30  * jrandom *baf*로 미팅을 종료한다 </div>
