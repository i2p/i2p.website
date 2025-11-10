---
title: "I2P 개발자 회의 - 2016년 2월 2일"
date: 2016-02-02
author: "zzz"
description: "2016년 2월 2일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단 요약

<p class="attendees-inline"><strong>참석자:</strong> allyourbase, anonimal, C0B4, cacapo, comraden1, eche|on, EinMByte, hottuna, Hummingbird, Irc2PGuest39432, Irc2PGuest76545, Irc2PGuest95462, IrcI2Pd743, JIa3apb_KaraHoBu4, lazygravy, nda, orignal, psi, sadie_i21, str4d, supervillain, The_Tin_Hat, trolly, xcps, Yankee, z3r0fox, zab\__, zzz</p>

## 회의 기록

<div class="irc-log">20:00:00 &lt;zzz&gt; 안건 http://zzz.i2p/topics/2014
20:00:00 &lt;zzz&gt; 0) 안녕
20:00:00 &lt;zzz&gt; 1) 12월 30일 회의에서 할당된 작업 검토 - http://zzz.i2p/topics/2016 (zzz)
20:00:00 &lt;zzz&gt; 2) 기타 CCC 후속 조치 - http://zzz.i2p/topics/2019 (zzz)
20:00:00 &lt;zzz&gt; 3) 2016 프로젝트 회의 계획 (zzz, Sadie)
20:00:00 &lt;zzz&gt; 4) GMP 6 병합 준비 상태  - http://zzz.i2p/topics/1960 (tuna)
20:00:00 &lt;zzz&gt; 5) http://secure.tinhat.i2p 콘솔 홈 페이지 요청 - http://zzz.i2p/topics/236?page=3#p10884 (david)
20:00:00 &lt;zzz&gt; 6) 행동 강령(Code of Conduct) 제안 - http://zzz.i2p/topics/2015 (Sadie)
20:00:02 &lt;lazygravy&gt; ccc 블로그 글에 그에 대한 링크가 있어요
20:00:05 &lt;zzz&gt; 0) 안녕
20:00:09 &lt;zzz&gt; 안녕
20:00:19 &lt;EinMByte&gt; 안녕
20:00:21 &lt;psi&gt; 안녕
20:00:25 &lt;lazygravy&gt; 안녕하세요
20:00:32 &lt;cacapo&gt; 안녕
20:00:33 &lt;sadie_i21&gt; 안녕
20:00:37 &lt;zzz&gt; 1) 12월 30일 회의에서 할당된 작업 검토 - http://zzz.i2p/topics/2016 (zzz)
20:00:44 &lt;Irc2PGuest76545&gt; 안녕
20:00:48 &lt;zzz&gt; 좋아요, 열린 항목들만 빨리 훑어봅시다
20:00:49 &lt;anonimal&gt; 안녕
20:00:50 &lt;Hummingbird&gt; 안녕
20:00:55 &lt;z3r0fox&gt; 안녕
20:01:03 &lt;zzz&gt; gravy가 암호화된 leasesets에 대해 1월 27일까지 하나 게시하기
20:01:11 &lt;zzz&gt; lazygravy, 진행 상황은?
20:01:34 &lt;orignal&gt; 안녕
20:01:37 &lt;lazygravy&gt; zzz: 그건 많이 늦었습니다. 하지만 시작은 했어요. 계속 쓸 계획입니다
20:01:38 &lt;zab__&gt; 안녕
20:01:44 &lt;trolly&gt; 안녕
20:01:50 &lt;lazygravy&gt; 주제를 바꿀 수도 있지만, 내 요지는 같습니다
20:01:51 &lt;zzz&gt; lazygravy, 새 목표 날짜는요?
20:02:27 &lt;Irc2PGuest39432&gt; 이런
20:02:28 &lt;Irc2PGuest39432&gt; 안녕
20:02:37 &lt;lazygravy&gt; zzz: 프레지던츠 데이 주말?
20:02:52 &lt;zzz&gt; 그게 며칠이죠?
20:03:10 &lt;lazygravy&gt; 2월 15일
20:03:14 &lt;zzz&gt; 좋아요, 고마워요
20:03:17 &lt;zzz&gt;  Sadie가 J와 협력하여 그의 블로그 글을 게시하기 
20:03:32 &lt;zzz&gt; sadie_i21,진행 상황?
20:03:42 &lt;sadie_i21&gt; 2월 중순
20:03:55 &lt;supervillain&gt; 보드카 마실 사람?
20:04:02 &lt;zzz&gt; Sadie가 backup에게 연락하여 reseed 캠페인 논의
20:04:05 &lt;zzz&gt; sadie_i21,진행 상황?
20:04:12 &lt;Irc2PGuest76545&gt; 안녕
20:04:27 &lt;sadie_i21&gt; 아직이에요
20:04:39 &lt;zzz&gt; 새 마감일은요?
20:06:09 &lt;zzz&gt; 좋아요, 넘어가죠. sadie 알려주세요
20:06:10 &lt;sadie_i21&gt; 이것도 2월 중순
20:06:10 &lt;Irc2PGuest95462&gt; 안녕
20:06:13 &lt;zzz&gt; 네트워크 강화 - 홈페이지와 추가 페이지들
20:06:13 &lt;zzz&gt; ** str4d, gravy, cacapo: 사용 사례 추가, 우리가 무엇을 가장 잘하는지, 더 많은 "열정"과 "살"을 붙이고, Bote 추가/강조, 1월 말까지
20:06:17 &lt;zzz&gt; 좋아요 고마워요 sadie
20:06:31 &lt;zzz&gt; str4d, lazygravy, cacapo, 진행 상황?
20:07:08 &lt;cacapo&gt; 작업 중이지만 커뮤니티의 피드백이 필요하다고 생각해요
20:07:16 &lt;str4d&gt; 안녕
20:07:16 &lt;lazygravy&gt; cacapo++
20:07:22 &lt;Irc2PGuest76545&gt; hallo
20:07:40 &lt;zzz&gt; 새 마감일은요?
20:08:42 &lt;cacapo&gt; 그리고 최종 목적이 명확하지 않은 것 같아요. 블로그 글을 위한 건가요?
20:08:50 &lt;hottuna&gt; cacapo: 다시 한번 읽어봐야 하면 핑해줘요
20:08:50 &lt;cacapo&gt; 3월 1일
20:09:07 &lt;EinMByte&gt; 최종 사용자뿐만 아니라 연구자도 대상으로 해주세요
20:09:07 &lt;str4d&gt; 내가 보기엔 범위는 홈페이지와 "supported applications" 페이지를 수정하는 거죠, 맞나요?
20:09:18 &lt;zzz&gt; 내 기억이 맞다면 의도는 홈페이지를 강화하고, 필요하면 추가 페이지를 더하는 것이었어요. 블로그 글은 아닙니다
20:09:33 &lt;zzz&gt; sadie_i21, 좀 더 설명해주시겠어요?
20:09:34 &lt;EinMByte&gt; 그럼 됐네요
20:09:38 &lt;str4d&gt; 맞아요
20:09:47 &lt;cacapo&gt; 그럼 supo
20:09:59 &lt;cacapo&gt; supported applications 페이지인가요?
20:10:26 &lt;zzz&gt; 내 기억으로는 우선순위가 홈페이지였어요. 다른 페이지(신규든 아니든)로 번져도 괜찮습니다
20:10:55 &lt;cacapo&gt; 또 하나: PR을 위해 토렌트를 언급할까요?
20:11:06 &lt;zzz&gt; sadie가 덧붙일 게 없다면, 넘어가죠
20:11:22 &lt;zzz&gt; 토렌트를 언급할지 말지는 회의 밖에서 논의합시다
20:11:37 &lt;sadie_i21&gt; 없음
20:11:38 &lt;str4d&gt; sadie_i21, Simply Secure의 디자인 생각들도 여기와 관련 있을 것 같아요.
20:11:39 &lt;str4d&gt; 그들이 홈페이지에 대해 즉각적인 생각이 있다면, 사용 사례를 어떻게 작성하고 제시할지에 영향을 줄 거예요/
20:12:00 &lt;zzz&gt; comraden이 2월 말까지 "i2p story"를 편집/다듬기/강화/게시
20:12:06 &lt;sadie_i21&gt; 미안 zzz, 통화 중이라...
20:12:09 &lt;zzz&gt; comraden1, 일정대로 가고 있나요?
20:12:13 &lt;str4d&gt; cacapo, 네. 토렌트의 장점(예: Tails 새 버전 다운로드!)을 강조하죠
20:12:17 &lt;psi&gt; sadie_i21: press@geti2p.net 스팸 파이어호스를 이메일로 포워딩받고 있나요?
20:12:42 &lt;zzz&gt; psi, 그건 sadie랑 오프라인으로 부탁해요
20:12:45 &lt;sadie_i21&gt; 아니요, 아직
20:12:50 &lt;psi&gt; ㅇㅋ
20:13:09 &lt;zzz&gt; 좋아요, comraden1은 일정대로라고 가정하겠습니다
20:13:17 &lt;zzz&gt; 더 넓은 로드맵과 우선순위 결정 프로세스는 추후 결정(TBD)이지만, 진행 중인 프로젝트 회의에서 나올 것입니다 
20:13:26 &lt;comraden1&gt; zzz: 당신이 올린 글은 아직 못 봤어요, 앞서 말했듯 급한 일이 생겼거든요
20:13:50 &lt;zzz&gt; 그 항목은 나와 sadie의 일이니, 3) 항목으로 미룹시다
20:13:52 &lt;comraden1&gt; 이번 주에 히스토리를 살펴보고 당신과 lance에게 수정 사항을 다시 전달하겠습니다
20:14:05 &lt;zzz&gt; comraden1, 2월 말까지 가능한가요?
20:14:26 &lt;str4d&gt; zzz, 초안이 꽤 흥미롭더군요 :)
20:14:31 &lt;str4d&gt; cacapo, 웹사이트에서 보이는 방식에 관해, 연도 헤더와 섞어서(일종의 "장"으로 나누듯이) 구성하면 잘 맞을 것 같아요. 그러면 연도별로 탐색할 수도 있겠죠.
20:14:34 &lt;comraden1&gt; zzz: 지금으로서는 네요 :)
20:14:45 &lt;zzz&gt; sadie가 검토하고, 권고를 하거나 티켓 관리를 시작(언제까지?) 
20:14:55 &lt;zzz&gt; sadie_i21, 진행 상황? 마감일은?
20:15:55 &lt;zzz&gt; 아직 통화 중이라고 가정할게요, 회신 부탁합니다
20:16:05 &lt;zzz&gt; 4) Android -
20:16:05 &lt;zzz&gt; 1)과 비슷하게 코드이고 java router와 연결되어 있지만, 3)처럼 임시적으로 또는 str4d의 1인 쇼 상태이고, 일정이 뒤처져 있습니다. 
20:16:13 &lt;str4d&gt; @YrB1rd에게서 DM: "There. Are. So. Many."
20:16:24 &lt;str4d&gt; (며칠 전 얘기지만 느낌은 알죠 ;P)
20:16:57 &lt;zzz&gt; 이건 실제 할 일 목록은 아니었지만, str4d Android 개발을 어떻게 관리할지 제안이 있나요, 아니면 당신과/또는 sadie에게 더 구체적인 과제를 드려도 될까요?
20:17:09 &lt;str4d&gt; 네, 제가 주요 의존성인 모든 것들이 지난 4~5개월 동안 완전히 엉망이었습니다.
20:17:36 &lt;zzz&gt; 0.9.24 릴리스를 위한 목표와, Android를 더 잘 관리하는 방안에 대한 계획을 마련하는 또 다른 목표 시점을 제시해줄 수 있나요?
20:17:39 &lt;str4d&gt; 박사학위 논문을 쓰고 있었거든요.
20:18:08 &lt;str4d&gt; 이번 주 말 제출을 목표로 하고 있어서 그건 정리되겠지만, 그 이후에는 유급 업무도 맡게 됩니다.
20:18:23 &lt;zzz&gt; 2월 5일, 좋습니다
20:18:33 &lt;str4d&gt; 0.9.24: 이번 주말을 목표로 하겠습니다.
20:18:38 &lt;sadie_i21&gt; zzz - 티켓 질문으로 다시 돌아갈 수 있을까요 - 지금 반쯤만 여기 있어요
20:18:56 &lt;zzz&gt; 지금 돌아갈까요 아니면 나중에요?
20:19:16 &lt;sadie_i21&gt; 나중에요 
20:19:22 &lt;str4d&gt; 그 다음으로는: 느리더라도 목표 지향적인 개발을 할 수 있도록 더 나은 로드맵이 필요합니다. 지금은 "오, 또 I2P 릴리스가 다가오네, 릴리스할 수 있도록 Android 작업 좀 비워야겠다"는 식이거든요.
20:19:23 &lt;zzz&gt; 좋아요, 0.9.24는 주말 끝이 2월 7일입니다
20:19:48 &lt;zzz&gt; 좋아요 str4d, 로드맵을 언제까지 마련할 건가요?
20:20:42 &lt;zzz&gt; 1) 항목에 대해 더 있나요?
20:20:50 &lt;str4d&gt; 로컬, 저장소, Trac에 할 일들이 잔뜩 있어요. 제가 필요한 건 기획에 더 많은 눈입니다.
20:21:30 &lt;zzz&gt; 날짜조차 못 주겠다는 건 안 좋은 신호예요. 할 일 목록에서 초안 로드맵이라도 올릴 수 있나요?
20:21:34 &lt;str4d&gt; zzz, 3월 6일로 하죠. 더 일찍 초안을 만들 수 있겠지만, 제가 거기 있는 동안 다른 것들과 함께 로드맵 작업을 하게 될 것 같습니다.
20:21:40 &lt;zzz&gt; 좋아요, 3월 6일
20:21:44 &lt;zzz&gt; 1) 마지막 호출
20:21:57 &lt;zzz&gt; 2) 기타 CCC 후속 조치 - http://zzz.i2p/topics/2019 (zzz)
20:22:13 &lt;zzz&gt; 2)는 다른 중요한 후속 사항이 있을 경우를 대비한 자리표시자로 넣었습니다
20:22:18 &lt;str4d&gt; RWC에서 후속 연락해야 할 분들이 몇 있습니다
20:22:13 &lt;str4d&gt; (2)에 끼워넣기)
20:22:26 &lt;zzz&gt; Phillip Winter와 Sybil에 관해 서신을 주고받고 있어요
20:22:39 &lt;zzz&gt; 다른 흥미로운 후속 보고할 게 있나요?
20:23:02 &lt;eche|on&gt; 제 쪽에서는 없습니다
20:23:25 &lt;zzz&gt; 좋아요, 모두들 이메일을 보내거나 하려던 연구를 해보세요, 아직 늦지 않았습니다
20:23:26 &lt;anonimal&gt; VRP를 이번 회의에서 다루려 했나요?
20:23:26 &lt;eche|on&gt; 재정은 이번 주말에 업데이트될 겁니다(IMHO)
20:23:44 &lt;zzz&gt; VRP는 안건에 없어요, 시간이 남으면 7)로 추가할 수 있습니다
20:23:49 &lt;zzz&gt; 2) 마지막 호출
20:23:58 &lt;JIa3apb_KaraHoBu4&gt; Dear zzz  ! I am very grateful to you for the creation of this network because I have met wonderful people here and find rare content, for which our country is suspended for the genitals an apple tree. Long old are you!
20:23:58 &lt;C0B4&gt; 미안하지만, 누가 0.9.24의 안전성을 확인했는지 오래 기다리고 있어요, 아니면 당신들은 보통 사람들의 질문에는 답하지 않나요&gt;&gt;&gt; &lt;C0B4&gt; 미안한데, 누가 0.9.24의 안전성을 확인했나요
20:24:11 &lt;str4d&gt; RWC에서 후속 연락해야 할 분들이 몇 있습니다
20:24:13 &lt;str4d&gt; (2)에 억지로 끼워넣기)
20:24:31 &lt;zzz&gt; 3) 2016 프로젝트 회의 계획 (zzz, Sadie)
20:24:44 &lt;lazygravy&gt; 끼워넣는 김에, i2spy에 대해 str4d와 얘기해야 해요. 그건 나중에/오프라인으로
20:24:57 &lt;zzz&gt; 간단한 항목입니다. 12월 30일 회의에서 프로젝트 관리에 더 진지하게 임하기로 했습니다
20:25:03 &lt;zzz&gt; 월례 회의를 열기로 했고
20:25:14 &lt;zzz&gt; 누군가가 프로젝트 매니저 역할을 맡기로 했습니다
20:25:37 &lt;zzz&gt; 그래서 이번이 첫 번째 월례 회의이고, 매달 첫 번째 화요일 UTC 오후 8시에 진행됩니다
20:25:56 &lt;zzz&gt; 다음 달은 예외로, 3월 7일 목요일에 합니다
20:26:26 &lt;zzz&gt; 목표는 제가 잠시 동안 이 회의를 진행하다가, 몇 번 지나면 Sadie에게 넘겨 그녀가 프로젝트 매니저 역할을 맡는 것입니다
20:26:34 &lt;zzz&gt; 괜찮나요? 의견 있나요?
20:26:39 &lt;lazygravy&gt; 합리적으로 보입니다. 우리 모두가 책임감을 갖는 데 도움이 되길 바랍니다.
20:26:59 &lt;comraden1&gt; 라
20:27:03 &lt;comraden1&gt; lazygravy++
20:27:04 &lt;anonimal&gt; sadie_i21이 IRC에 더 자주 오게 되나요?
20:27:15 &lt;xcps&gt; C0B4, 좋은 지적!
20:27:15 &lt;lazygravy&gt; anonimal++
20:27:22 &lt;sadie_i21&gt; 알겠어요
20:27:33 &lt;str4d&gt; 좋아 보입니다
20:27:42 &lt;zzz&gt; 좋은 지적이에요, 우리가 sadie_i21에게 더 자주 오라고 반복해서 권했죠, 더 쉽게 하려고 두 번째 컴퓨터를 마련 중이었던 걸로 알아요
20:27:48 &lt;str4d&gt; sadie_i21, bouncer 계정 - sadie - 아직 가지고 있어요, 원하면 드릴게요
20:28:04 &lt;zzz&gt; 자주 여기 없으면 프로젝트 관리가 어려울 것 같아요
20:28:28 &lt;anonimal&gt; 안녕하세요 sadie_i21, 공식적으로 인사한 적은 없네요.
20:28:28 &lt;anonimal&gt; PM 관련 질문이 있지만, 기다려도 될 것 같아요?
20:28:30 &lt;str4d&gt; 최소한 PM 등을 놓치지 않게 해줄 거예요.
20:28:39 &lt;zzz&gt; sadie_i21, 여기 상주하고 스크롤백을 볼 수 있는 환경 구축은 진척이 있나요?
20:28:52 &lt;sadie_i21&gt; 안녕하세요! 더 자주 오려고 노력 중입니다!!
20:28:57 &lt;anonimal&gt; s/PM-related/Project Management-related/
20:29:06 &lt;comraden1&gt; str4d: 그 설정을 sadie_i21에게 해주는 방법을 나와 오프라인으로 얘기해줄래요? 트위터나 여기 모두 괜찮아요
20:29:14 &lt;sadie_i21&gt; 네, zzz - 다 끝났고 설정했어요
20:29:43 &lt;zzz&gt; 좋아요, 나에서 sadie로의 일반적인 이양 계획이 있으니, 향후 몇 달 동안 어떻게 되는지 봅시다
20:29:47 &lt;eche|on&gt; 방해해서 미안, sadie가 매니저가 될 거라면, 조직적으로 필요한 시스템이 있어야 해요
20:30:01 &lt;eche|on&gt; 필요한 하드웨어요, 미안
20:30:20 &lt;zzz&gt; echelon 응?
20:30:41 &lt;str4d&gt; comraden1, ㅇㅋ
20:31:00 &lt;zzz&gt; 3)에 더 있나요?
20:31:05 &lt;comraden1&gt; eche|on: 제가 컴퓨터를 하나 설정해줬어서 필요 없을 수도 있지만, 새 장비를 원한다면 그건 그녀의 선택이죠
20:31:14 &lt;eche|on&gt; zzz: 미안, 우리가 그녀가 필요한 PC 시스템에 대해 얘기했고, 내게 연락을 주면 좋겠다고 했어요
20:31:23 &lt;zzz&gt; 좋아요
20:31:29 &lt;zzz&gt; 4) GMP 6 병합 준비 상태  - http://zzz.i2p/topics/1960 (tuna)
20:31:35 &lt;zzz&gt; hottuna, 최신 상황은?
20:31:38 &lt;eche|on&gt; 그게 쟁점이라면, 내 생각엔 괜찮습니다만, 여기 회의에서 찬성 투표할 수 있어요!
20:31:56 &lt;hottuna&gt; Windows x86에서 jcpuid가 작동하지 않아요
20:32:05 &lt;hottuna&gt; 테스트할 선택지가 두 개 남았고, 그 뒤엔 정말 아이디어가 100% 없습니다
20:32:40 &lt;zzz&gt; 좋아요. kytv가 5년 전에 성공했으니, 막히면 그가 도와줄 수 있을지도 몰라요
20:32:48 &lt;eche|on&gt; jcpuid가 C 코드인가요?
20:32:58 &lt;hottuna&gt; osx용 ucpuid는 컴파일도 테스트도 안 했어요
20:32:58 &lt;hottuna&gt; jcpuid*
20:33:13 &lt;hottuna&gt; c+asm+java-bindings
20:33:13 &lt;zzz&gt; 이런 큰 변경은 0.9.25에 넣을 수 있도록 2월 중순까지 준비되었으면 합니다. 그러려면 약 2주 남았어요
20:33:24 &lt;anonimal&gt; hottuna: 그건 도와줄 수 있어요.
20:33:31 &lt;str4d&gt; 살펴볼 수 있는 또 다른 대안도 있어요
20:33:41 &lt;hottuna&gt; zzz: 장담은 못 하겠어요. 좀 벽에 부딪혔습니다
20:33:47 &lt;hottuna&gt; anonimal: osx 빌드를 도와주실 수 있나요?
20:33:48 &lt;str4d&gt; orignal이 얼마 전 우리 ElGamal 구현을 훨씬 더 효율적으로 만들 수 있다는 점을 제기했죠.
20:33:52 &lt;hottuna&gt; 아니면 windows x86을 도와주실 수 있나요?
20:34:02 &lt;hottuna&gt; str4d: 어떻게요?
20:34:04 &lt;str4d&gt; (현재는 ElG 연산을 그냥 직접 합니다)
20:34:07 &lt;hottuna&gt; 전부 C로 하면요?
20:34:12 &lt;zzz&gt; 회의 중에는 ElG 얘기로 새지 맙시다
20:34:17 &lt;zzz&gt; 회의에서는요
20:34:25 &lt;str4d&gt; hottuna, 예를 들어 Montgomery ladder 같은 걸 사용하는 식으로요
20:34:30 &lt;str4d&gt; 아직 검토가 필요합니다
20:34:35 &lt;hottuna&gt; 알겠어요
20:34:41 &lt;IrcI2Pd743&gt;  C0B4 예를 들면, 아무도요. 사람들은 네트워크의 안전성과 익명성에 대해 말만 믿습니다.
20:34:53 &lt;zzz&gt; 요약하면 hottuna에게 도움이 필요하고 시간도 촉박해서 .25를 놓칠 수 있습니다. 부탁이 오면 모두 도와주세요
20:35:00 &lt;anonimal&gt; hottuna: 네. 요즘 Kovri 때문에 항상 시간이 빠듯하지만, 가능한 만큼 하겠습니다.
20:35:08 &lt;zzz&gt; 4) 더 있나요?
20:35:14 &lt;anonimal&gt; hottuna: 최신 링크가 포럼 글에 있나요?
20:35:34 &lt;str4d&gt; 테스트에는 제가 도움이 안 돼서 안타깝네요
20:35:36 &lt;hottuna&gt; 어떤 링크요?
20:35:40 &lt;hottuna&gt; jcpuid요?
20:35:47 &lt;orignal&gt; str4d, 100%
20:36:18 &lt;zzz&gt; 5) http://secure.tinhat.i2p 콘솔 홈 페이지 요청 - http://zzz.i2p/topics/236?page=3#p10884 
20:36:27 &lt;zzz&gt; The_Tin_Hat, 사이트에 대해 말씀해 주세요
20:37:10 &lt;JIa3apb_KaraHoBu4&gt; 정당화는 약자들을 위한 것!
20:37:16 &lt;The_Tin_Hat&gt; 이 사이트는 프라이버시와 보안에 대한 여러 실용적인 튜토리얼을 제공하며, 중급 사용자가 소화할 수 있도록 작성되어 있습니다. I2P와 Tor에 관한 튜토리얼도 몇 가지 포함되어 있습니다
20:38:03 &lt;The_Tin_Hat&gt; I2P 및/또는 인터넷 보안과 프라이버시에 이제 막 입문하는 사람들에게 적합하다고 생각합니다
20:38:03 &lt;zzz&gt; thetinhat.i2p는 한동안 운영해 온 걸로 아는데, 비교적 새로 생긴 secure.thetinhat.com은 무엇인가요? 각각 얼마나 되었나요?
20:38:08 &lt;trolly&gt; thetinhat을 예전부터 압니다
20:38:18 &lt;trolly&gt; 그 튜토리얼 몇 개를 번역했어요
20:38:23 &lt;str4d&gt; zzz, 내가 이해하기로는 secure.thetinhat.i2p는 EdDSA 키예요
20:38:44 &lt;The_Tin_Hat&gt; thetinhat.i2p는 여전히 존재하고, 서버를 바꾸고 키를 업그레이드하면서, 더 긴 tunnels와 함께 서브도메인을 추가했습니다
20:38:53 &lt;C0B4&gt; 미안한데, 질문에 대한 답을 오래 기다리고 있어요, 아니면 당신들은 보통 사람들에겐 답을 안 하나요&gt;&gt;&gt; &lt;C0B4&gt; 미안한데, 누가 0.9.24의 안전성을 확인했나요
20:38:53 &lt;zzz&gt; 이 요청에 대해 질문이나 의견이 있나요?
20:38:57 &lt;str4d&gt; 그래서 5a) 키 업그레이드를 가능하게 하려면 구독 피드를 확장해야 합니다
20:39:16 &lt;zzz&gt; C0B4, 지금 회의 중입니다, 미안해요
20:39:43 &lt;zzz&gt; str4d, 5a)는 다음 달 로드맵 회의에서 얘기합시다
20:39:52 &lt;str4d&gt; ㅂ
20:40:15 &lt;str4d&gt; 추가에 +1입니다.
20:40:47 &lt;hottuna&gt; +1, 추가합시다
20:40:52 &lt;anonimal&gt; hottuna: 네, jcpuid요.
20:40:56 &lt;zzz&gt; 좋아요 secure.thetinhat.i2p 콘솔 홈 페이지 요청에 대해, 다른 질문이나 의견이 없으면 +1 또는 -1로 투표해 주세요
20:40:59 &lt;lazygravy&gt; +1
20:41:13 &lt;Yankee&gt; Hi, gays!
20:41:23 &lt;trolly&gt; +1
20:41:23 &lt;cacapo&gt; +1
20:41:51 &lt;comraden1&gt; 추가에 +1
20:41:53 &lt;anonimal&gt; hottuna: 아니면 지금은 mtn에서 바로 작업하나요? (마지막으로 테스트한 이후로 본 게 없네요)
20:42:24 &lt;zzz&gt; anonimal, 그 주제에서 벗어났으니 다른 곳에서 논의해 주세요, 감사합니다
20:42:32 &lt;zzz&gt; 좋아요 5) 마지막 호출
20:42:37 &lt;z3r0fox&gt; +1
20:43:06 &lt;zzz&gt; 이의가 없으므로 thinhat 요청을 승인하겠습니다. .25에 반영하겠습니다
20:43:27 &lt;zzz&gt; 6) 행동 강령(Code of Conduct) 제안 - http://zzz.i2p/topics/2015 (Sadie)
20:43:27 &lt;zzz&gt; 6a) 제안과 그 이유 (Sadie)
20:43:27 &lt;zzz&gt; 6b) Sadie에게 질문
20:43:27 &lt;zzz&gt; 6c) zzz.i2p에 아직 댓글을 달지 않은 분들의 간단한 코멘트
20:43:27 &lt;zzz&gt; 6d) zzz.i2p에 이미 댓글을 단 분들의 간단한 코멘트
20:43:27 &lt;zzz&gt; 6e) 다음 회의에서 구체적 제안을 제시할 자원봉사자
20:43:50 &lt;zzz&gt; 이 주제는 약 20분으로 제한하고 싶습니다. 오늘 최종 결정은 하지 않을 겁니다
20:43:53 &lt;zzz&gt; 6a) 제안과 그 이유 (Sadie)
20:44:01 &lt;zzz&gt; sadie_i21, 시작해 주세요
20:45:30 &lt;zzz&gt; sadie를 놓쳤네요, 6b로 넘어갑시다
20:45:36 &lt;zzz&gt; 아니, 6c로
20:45:40 &lt;Yankee&gt; zzz:  Edward Snowden이 i2p는 안전하지 않다고 썼어요
20:45:44 &lt;zzz&gt; 6c) zzz.i2p에 아직 댓글을 달지 않은 분들의 간단한 코멘트
20:46:09 &lt;zzz&gt; 아직 zzz.i2p 스레드에 의견을 남기지 않았다면, 지금 이 제안에 대해 코멘트해 주세요
20:46:13 &lt;orignal&gt; 6, 내 생각에 CoC는 전혀 쓸모없습니다
20:46:32 &lt;orignal&gt; 성인은 그런 기준을 머릿속에 갖고 있어야 합니다
20:47:02 &lt;orignal&gt; 정책이나 CoC 및 기타 HR의 그런 sh#t을 만들기보다는
20:47:29 &lt;comraden1&gt; zzz: 난 coc에 찬성이에요 (NSA의 coc를 예시로 lazygravy가 링크를 올렸어요). 이는 개발의 프로젝트 성숙도의 일부이며, i2p에 프로그래머뿐만 아니라 더 많은 사람이 참여할 수 있게 하기 위한 것입니다
20:47:41 &lt;orignal&gt; 정책 대신 일을 하세요
20:47:53 &lt;eche|on&gt; 제 입장은, 우리 모두가 이미 동의한 것처럼, 적어도 문서화하고 불문율을 고정할 수 있다는 겁니다. 아무 변화도 없어요.
20:48:02 &lt;anonimal&gt; zzz: 저는 CoC에 찬성입니다.
20:48:04 * orignal 은(는) 프로그래머가 줄어들 거라고 믿습니다
20:48:04 &lt;zzz&gt; zzz.i2p 스레드에 아직 코멘트하지 않은 다른 분들, 의견을 덧붙이고 싶으신가요?
20:48:16 &lt;zzz&gt; 코멘트는 간단히 해 주세요
20:49:05 &lt;orignal&gt; 간단히 말하면, i2pd에는 CoC를 도입하지 않을 것입니다.
20:49:18 &lt;zzz&gt; 좋아요. 6a)로 돌아갑시다. sadie_i21, 제안과 생각, 그리고 이유를 알려주세요
20:49:19 &lt;orignal&gt; 끝.
20:50:15 &lt;Yankee&gt; anonimal: 너보다 더 지루한 사람은 본 적 없어...
20:50:24 &lt;EinMByte&gt; 아마 CoC가 아주 중요하진 않지만, 반대하지는 않습니다.
20:50:24 &lt;EinMByte&gt; 일종의 형식에 가깝죠
20:50:40 &lt;anonimal&gt; 한 가지 코멘트:
20:50:43 &lt;anonimal&gt; CoC는 피해자만 보호하는 게 아니라, 가해자가 경력이나 개인 생활에 장기적으로 악영향을 미칠 어리석은 결정을 내리는 것도 막아줍니다.
20:50:43 &lt;anonimal&gt; 스레드에서 더 코멘트할 수 있어요. 끝.
20:50:56 &lt;zzz&gt; 좋아요, 6d) zzz.i2p 스레드에 이미 코멘트했더라도, 여기서 다른 코멘트를 자유롭게 해 주세요
20:51:18 &lt;zzz&gt; 스레드에서 명확하지 않았거나 더 덧붙이고 싶은 생각이 있나요?
20:52:03 &lt;sadie_i21&gt; 커뮤니티 기준을 두는 것에 대한 피드백을 구하고 있었어요 
20:52:04 &lt;EinMByte&gt; anonimal: 맞아요, 하지만 대부분의 가해자는 익명일 겁니다.
20:53:00 &lt;allyourbase&gt; 무엇에 사용할 건가요? 기자들에게 보내나요? 프로젝트 구성원을 퇴출하나요?
20:53:02 &lt;sadie_i21&gt; zzz의 말처럼, 프로젝트 성숙도에 맞춰서요
20:53:08 &lt;lazygravy&gt; 나도 EinMByte와 비슷하게 느껴요. 쓸모없거나 좋거나 둘 중 하나지, 일부가 말하듯 세상이 무너질 일은 아니에요
20:53:08 &lt;lazygravy&gt; 쓸모없다는 건 순 효과가 0이라는 뜻이지, 마이너스는 아니라는 말
20:53:08 &lt;C0B4&gt; anonimal, 그는 선험적으로 범죄자다. 왜 그를 변호하나&
20:53:09 &lt;zzz&gt; sadie, 표준이나 CoC 자체에 대한 일반적인 피드백을 원한 거죠? 아직(은) 검토할 구체적인 예시는 제시하지 않았네요
20:53:26 &lt;comraden1&gt; EinMByte: 이상적으로는 이를 다루는 방법부터 시작할 수 있어요. 이걸 다시 링크합니다 https://github.com/NationalSecurityAgency/SIMP/blob/master/Community_Code_of_Conduct.md 가이드라인 위반 부분은 우리가 시행할 수 있다고 봅니다
20:53:31 &lt;psi&gt; 내 생각엔 CoC는 쓸모없고 자충수입니다
20:53:37 &lt;EinMByte&gt; anonimal: 음, 사람들 기분 상하게 할 작정이라면 익명으로 남는 게 현명하겠죠 ;).
20:53:39 &lt;psi&gt; PR 측면에서요
20:53:39 &lt;Yankee&gt; zzz: 러시아 사람이 C++로 클라이언트를 썼다고 했어요. 사실인가요?
20:53:57 &lt;zzz&gt; Yankee, 지금 회의 중입니다, 미안해요
20:54:00 &lt;sadie_i21&gt; 또, 추후 보조금 등에 신청할 때 도움이 될까요
20:54:21 &lt;EinMByte&gt; sadie_i21: 그럴 수도 있겠네요, 좋은 지적입니다.
20:54:33 &lt;zab__&gt; 진짜요? 보조금은 중요해요
20:54:34 &lt;psi&gt; 그리고 내가 FUD를 퍼뜨린다고 비난받았죠 
20:54:38 &lt;lazygravy&gt; Debian과 수천 개의 다른 프로젝트도 CoC를 쓰고 있고 PR도 괜찮아요. 이걸 어떻게 반박하죠?
20:54:39 &lt;sadie_i21&gt; 어쨌든, 이건에 대해 포럼에 아이디어를 공유해준 모두에게 감사해요
20:54:50 &lt;anonimal&gt; Yankee: Pashol na xyi :)
20:54:53 * orignal 은 zab__의 의견에 동의합니다
20:55:22 * orignal 은 방금 anonimal의 말 때문에 CoC에 찬성합니다
20:55:30 &lt;psi&gt; lazygravy: saddie는 당신이 절대 일어나지 않을 거라고 했던 커뮤니티 기준을 방금 제안했어요
20:55:33 &lt;comraden1&gt; zab__: 이게 sadie_i21가 말한 건데, 미국 NSF의 새로운 입장입니다 https://www.nsf.gov/news/news_summ.jsp?cntn_id=137466
20:55:41 &lt;anonimal&gt; sadie_i21: 우리에게 알려줘서 고마워요.
20:55:59 &lt;str4d&gt; sadie_i21, 전체 커뮤니티를 뜻하나요, 아니면 개발 커뮤니티만요?
20:56:00 &lt;lazygravy&gt; psi: 그 FUD는 그만둬야 해요. 개발 커뮤니티를 말한 거예요
20:56:01 &lt;zzz&gt; 좋아요, sadie_i21 다음 회의에 구체적 제안을 가져오고 싶나요? 아니면 진행하지 않을까요? 다음 단계는요?
20:56:09 &lt;Yankee&gt; anonimal: 뭐요?
20:56:11 &lt;psi&gt; lazygravy: 그건 FUD가 아니에요...
20:56:24 &lt;orignal&gt; 모두들, 미안하지만 여기서 욕설이 허용된다고 생각하나요?
20:56:32 &lt;sadie_i21&gt; 전체 커뮤니티는 아니에요 - 아니요.
20:56:44 &lt;nda&gt; CoC. '나쁜 사람'에게 기술적으로 무엇을 할 건가요? (제 영어 죄송)
20:56:44 &lt;IrcI2Pd743&gt; sadie_i21, r u not a HR for a living?
20:57:06 &lt;lazygravy&gt; psi: 맞아요. 하지만 이건 오프라인에서 논의합시다.
20:57:09 * zab__ 미소 짓는다
20:57:25 &lt;zab__&gt; Yankee: ,  
20:57:25 &lt;nda&gt; 정부에 편지라도 보낼 건가요, 아니면 뭐죠?
20:57:34 &lt;C0B4&gt; an
20:57:45 &lt;psi&gt; CoC는 i2p에 잘못된 선택입니다
20:57:52 &lt;zzz&gt; 여기와 zzz.i2p 스레드의 코멘트를 고려해 다음 달에 구체적 제안 작업을 할 자원봉사자가 있나요?
20:57:52 &lt;C0B4&gt; anonimal,       ?
20:58:07 &lt;orignal&gt; zab__,         
20:58:15 &lt;eche|on&gt; nda: 최종적으로는, 일정 기간 우리 Java 메인 포크 개발 작업에서 제외하는 식?
20:58:17 &lt;IrcI2Pd743&gt; anonimal,  . , -,  , .  ?
20:58:21 &lt;zzz&gt; 여러분, 주제에 집중해 주세요, 영어로 부탁합니다, 감사합니다
20:58:23 &lt;sadie_i21&gt; 다음 회의 때 제안을 만들어봅시다
20:58:40 &lt;zzz&gt; 좋아요, sadie와 함께할 자원봉사자 있나요?
20:58:44 &lt;orignal&gt; zzz, anonimal이 먼저였어요
20:58:53 &lt;IrcI2Pd743&gt; zzz, 미안, 하지만 당신이 먼저 개발자죠
20:58:56 &lt;comraden1&gt; zzz: 자료 링크 등으로 누구든 도울 수 있어요. 제 삶이 지금 무너지고 있어서 모든 일을 맡겠다고 약속할 수는 없어요 :)
20:58:58 &lt;orignal&gt; 모두에게 매우 모욕적인 말을 했어요
20:59:02 &lt;IrcI2Pd743&gt; *your
20:59:04 &lt;nda&gt; eche|on 아, 답변 고마워요
20:59:10 &lt;zab__&gt; CoC를 꼼꼼히 읽고 의견을 내겠다고 약속합니다
20:59:19 &lt;anonimal&gt; zzz sadie_i21: 돕고 싶습니다.
20:59:35 &lt;lazygravy&gt; 우리는 특정 문구에 아직 합의하지는 않았다고 생각해요
20:59:48 &lt;anonimal&gt; VRP나 문서 재작성/재정리보다 Java I2P에 조금 더 시간을 써야겠어요.
20:59:49 &lt;lazygravy&gt; (문구는 매우 중요하다고 봐요. 엉망으로 쓰일 수도 있거든요)
21:00:04 &lt;zzz&gt; 요약하면 '팀 구성원'(체크인 권한 보유자나 팀 페이지에 있는 사람) 중에는 찬성이 더 많고, 팀 외부에서는 반대가 더 많은 것 같습니다
21:00:21 &lt;str4d&gt; lazygravy, 맞아요. 그리고 다음 회의에서 특정 문구에 합의하리라고도 생각하지 않아요
21:00:21 &lt;str4d&gt; meeting*
21:00:25 &lt;zzz&gt; 두 집단 모두 중요합니다. 비팀원이 팀원이 될 수도 있으니까요
21:00:39 &lt;zab__&gt; 이상적으로는 하나 이상의 후보 CoC를 마련했으면 합니다
21:00:41 &lt;str4d&gt; 여러 제안이 있고, 찬반 이유도 다양하다고 봅니다.
21:01:13 &lt;zzz&gt; 코드나 프로세스에 대해 최종 판단은 제가 하게 될 가능성이 크므로, 폭넓거나 거의 만장일치에 가까운 합의가 없는 것은 채택하고 싶지 않습니다
21:01:21 &lt;str4d&gt; 좋은 출발점은 제안된 옵션들을 몇 사람이 장단점을 검토하는 것입니다
21:01:38 &lt;zzz&gt; 좋아요, sadie 다음 달에 무엇인가를 가져오는 과제가 당신에게 배정된 듯합니다
21:01:44 &lt;zzz&gt; 6)에 더 있나요?
21:02:02 &lt;sadie_i21&gt; 메모했습니다
21:02:10 &lt;str4d&gt; CoC 또는 유사한 것들에 대한 긍정/부정 인식(예: 위의 보조금 문제나 주요 반대 사유처럼 보이는 부정적 인상)에 관한 추가 조사가 유용할 겁니다
21:02:16 &lt;EinMByte&gt; 실제 제안을 보기 전에는 결정을 못 하겠어요
21:02:17 &lt;str4d&gt; 하지만 그건 더 많은 노력이 필요하죠
21:02:34 &lt;nda&gt; 그리고 CoC로, i2p 팀에 속하지 않은 '나쁜 사람들'에게는 아무것도 할 수 없나요?
21:02:44 &lt;zzz&gt; 6) 마지막 호출
21:02:57 &lt;lazygravy&gt; str4d++
21:03:09 &lt;str4d&gt; nda, CoC든 무엇이든 I2P 개발 팀에만 해당합니다, 네
21:03:25 * lazygravy 잠시 자리 비움, 현실에서 일이 생김
21:03:27 &lt;eche|on&gt; nda: 왜 그래야 하죠? 이건 우리 i2p-dev-team을 위한 겁니다
21:03:29 &lt;str4d&gt; 요컨대, 우리는 더 많은 데이터가 필요합니다.
21:03:40 &lt;nda&gt; str4d 알겠어요, 고마워요
21:03:44 &lt;psi&gt; (일단은)
21:03:45 &lt;comraden1&gt; zab__: 나쁘지 않은 생각이네요. 직접 만들기보다는 복사해 쓸 수 있는 것들을 살펴보는 게 이치에 맞습니다
21:03:49 &lt;zzz&gt; 좋아요, 6)을 마치겠습니다, 모두 감사합니다
21:03:59 &lt;zzz&gt; 7) VRP anonimal 진행하세요
21:04:03 &lt;str4d&gt; 본질적으로는 우리가 이미 서명해야 하는 개발자 협약의 확장이 될 것입니다.
21:04:40 &lt;anonimal&gt; VRP 관련: zzz와 str4d, 그리고 커뮤니티의 응답을 기다리고 있습니다.
21:04:57 &lt;anonimal&gt; 그러면 티켓을 다시 작성하고 마무리할 수 있어요.
21:04:59 &lt;nda&gt; 저는 이게 "경찰 불러요, I2P에 나쁜 사람이 있어요!" 같은 건 줄 알았어요, 정말 미안해요 )
21:05:01 &lt;comraden1&gt; 그리고 str4d의 말에 덧붙이면, 개발자 협약에 서명하지 않은 사람들(저처럼)을 위한 최소 기준도 보장하겠죠
21:05:08 &lt;str4d&gt; anonimal, 오, 추가 업데이트가 있었나요? 놓쳐서 미안해요.
21:05:09 &lt;zzz&gt; 지금 티켓 번호가 손에 없네요. 무엇이 필요하죠? str4d가 최근 Kate와 만난 걸로 알아요. str4d 최신 상황은?
21:05:26 &lt;eche|on&gt; what is VRP`
21:05:26 &lt;eche|on&gt; ?
21:05:36 &lt;str4d&gt; eche|on, Vulnerability Response Process
21:05:37 &lt;anonimal&gt; http://trac.i2p2.i2p/ticket/1119
21:05:37 &lt;zzz&gt; anonimal, 그 티켓이 당신 건가요?
21:05:39 &lt;eche|on&gt; 아, 좋아요
21:05:52 &lt;eche|on&gt; 복잡한 주제죠
21:06:04 &lt;zzz&gt; 아직 H1을 쓸지조차 결정하지 않았죠, 그렇죠? 하지만 분명 최근에 큰 반향을 일으켰습니다
21:06:15 &lt;str4d&gt; zzz, 오픈소스 버그 바운티 프로그램과 관련해 Katie와 아직 후속 연락을 못 했는데(논문), 이번 주에 하겠습니다.
21:06:38 &lt;str4d&gt; 그녀에게 좋은 인상을 받았고, 티켓에서의 응답도 좋았습니다
21:06:38 &lt;zzz&gt; 다음 달 로드맵 회의에서 이걸 확실히 결정하는 게 좋을까요?
21:06:40 &lt;anonimal&gt; 그게 가장 큰 장애물이었던 것 같아요: H1 결정.
21:06:40 &lt;anonimal&gt; 티켓에 그들이 댓글을 달았고, 그들의 주장을 했고, 
21:06:41 &lt;anonimal&gt; 제 주장을 했고,
21:06:43 &lt;anonimal&gt; kay도 그들의 주장을 했고,
21:06:52 &lt;str4d&gt; Katie도 우리가 거치는 프로세스에 대해 좋은 코멘트를 했습니다
21:07:33 &lt;zzz&gt; 3월 전에 결정을 내릴 만큼 집중할 수 있을지 모르겠네요. 티켓의 세부 내용이 좀 벅찹니다. 너무 많은 것 같기도 해요. 하지만 어쩌면 아닐 수도 있고요.
21:08:02 &lt;zzz&gt; str4d, 이걸 어떻게, 언제 다루어야 할까요?
21:08:37 &lt;str4d&gt; 참고로, 우리가 이걸 제대로 하려고 세부사항과 수고를 들이는 걸 Katie는 좋게 봤습니다
21:08:52 &lt;zzz&gt; 좋아요, 하지만 난 Katie의 생각보다 당신 생각이 더 중요해요 :)
21:09:05 &lt;str4d&gt; zzz, Tor가 참여한 것과 같은 버그 바운티 프로그램에 우리가 들어갈 수 있다면, 그게 아마 우리 결정을 사실상 내려줄 겁니다
21:09:09 &lt;zzz&gt; 어떻게, 언제 답을 얻죠
21:09:37 &lt;str4d&gt; 무료 페이지만 두는 것보다 연구자 유입이 더 많을 거라 생각하거든요
21:09:47 &lt;anonimal&gt; 이게 12월 회의에서 연기됐었으니, 또 연기되는 건 신나진 않네요
21:09:47 &lt;anonimal&gt; 하지만 정말로 제가 이래라저래라 하거나 요청할 처지는 아닙니다.
21:09:47 &lt;anonimal&gt; 그래서, 모두에게 맞는 방향으로요.
21:09:47 &lt;anonimal&gt; s/exciting/excited/
21:09:55 &lt;zzz&gt; 네, 하지만 H1과 무관하게, 우리는 프로세스가 필요합니다
21:10:04 &lt;str4d&gt; 맞아요
21:10:24 &lt;zzz&gt; 그래서 3월 로드맵 회의에서 작업하자고 제안합니다. 괜찮을까요?
21:10:31 &lt;str4d&gt; 다음 주에 anonimal의 최신 변경을 검토하겠습니다.
21:10:41 &lt;zzz&gt; 좋아요, 저도 그렇게 하겠습니다
21:10:49 &lt;zzz&gt; 7) 더 있나요?
21:10:54 &lt;str4d&gt; 2월 12일까지
21:11:02 &lt;IrcI2Pd743&gt; anonimal, 내 주변에서 욕설을 허용한 것은 좌절감을 줬습니다.
21:11:18 &lt;anonimal&gt; 내 마지막 4줄이 전달됐나요?
21:11:18 * comraden1 잠시 자리 비움
21:11:29 &lt;zzz&gt; 회의에 더 있을 것이 있나요?
21:11:32 &lt;str4d&gt; anonimal, s/까지 봤어요
21:11:40 &lt;IrcI2Pd743&gt; anonimal, 사과를 요구합니다.
21:11:42 * zzz *baffer를 예열한다
21:11:52 &lt;anonimal&gt; 회의 로그를 검토할게요, 놓친 텍스트가 많은 것 같습니다.
21:11:57 &lt;orignal&gt; 8) anonimal의 말
21:12:09 * zzz *bafffs* 회의를 종료했다 </div>
