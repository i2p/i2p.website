---
title: "I2P 개발자 회의 - 2016년 3월 3일"
date: 2016-03-03
author: "zzz"
description: "2016년 3월 3일자 I2P 개발 회의 로그."
categories: ["meeting"]
---

## 간단 요약

<p class="attendees-inline"><strong>참석자:</strong> anonimal, comraden1, eche|on, hottuna4, orignal\_, sadie_i2p, str4d, Yankee, zzz</p>

## 회의 기록

<div class="irc-log">20:00:02 &lt;zzz&gt; 0) 안녕하세요
20:00:02 &lt;zzz&gt; 1) 12월 30일 회의에서 할당되었지만 아직 열린 작업 검토 http://zzz.i2p/topics/2014
20:00:02 &lt;zzz&gt; 2) 2월 2일 회의에서 새로 할당된 작업 검토 http://zzz.i2p/topics/2014
20:00:02 &lt;zzz&gt; 3) 로드맵 미팅 준비 및 일정 http://zzz.i2p/topics/2021
20:00:02 &lt;zzz&gt; 4) 행동 강령(Code of Conduct) 제안 (Sadie) http://zzz.i2p/topics/2015?page=2
20:00:12 &lt;zzz&gt; 0) 안녕하세요
20:00:15 &lt;zzz&gt; 안녕
20:00:25 &lt;anonimal&gt; 안녕
20:00:38 &lt;str4d&gt; 안녕
20:01:07 &lt;zzz&gt; 1) 12월 30일 회의에서 할당되었지만 아직 열린 작업 검토 http://zzz.i2p/topics/2014
20:01:19 &lt;hottuna4&gt; 안녕
20:01:37 &lt;zzz&gt; gravy가 1월 27일까지 encrypted leasesets에 관한 글을 하나 올리거나, 다른 주제라면 2월 15일까지 올리기로 함
20:01:51 &lt;zzz&gt; gravy의 근황 아는 사람?
20:03:13 &lt;anonimal&gt; 아니요.
20:03:47 &lt;sadie_i2p&gt; 현실에서 바쁨
20:04:07 &lt;zzz&gt; sadie_i2p, 그에게서 새로운 예정일 받았나요?
20:04:24 &lt;sadie_i2p&gt; Gravy에게 새 날짜를 기다리는 중
20:04:33 &lt;zzz&gt; 좋아요, 다음 회의로 넘기겠습니다
20:04:42 &lt;zzz&gt; Sadie가 J와 함께 그의 reseed 블로그 포스트를 올리기로 함, 새 날짜는 2월 중순.
20:04:49 &lt;zzz&gt; sadie_i2p, 진행 상황이 어떤가요?
20:05:42 &lt;sadie_i2p&gt; J도 바빠요, Back up과 함께 작업 중
20:06:07 &lt;zzz&gt; sadie_i2p, 이 시점에 블로그 포스트가 가능할까요, 아니면 넘어갈까요?
20:06:44 &lt;sadie_i2p&gt; 지금은 back up과 제가 다른 것을 작업 중이라 - 블로그 포스트는 아마도 없을 것 같아요
20:06:58 &lt;zzz&gt; 좋아요, 목록에서 지우겠습니다
20:07:02 &lt;sadie_i2p&gt; 넘어가죠
20:07:17 &lt;zzz&gt; Sadie가 backup과 reseed 캠페인 논의, 새 날짜는 2월 중순.
20:07:32 &lt;zzz&gt; sadie_i2p, 당신과 backup은 무엇을 준비 중인가요?
20:07:34 &lt;anonimal&gt; 2월?
20:07:54 &lt;zzz&gt; 네 anonimal, 이건 모두 기한이 지난 항목들이에요
20:08:26 &lt;sadie_i2p&gt; 새 콘텐츠와 그래픽 
20:08:51 &lt;zzz&gt; 웹사이트용이라고 생각해요
20:08:55 &lt;sadie_i2p&gt; 일정 때문에 지연이 있을 거예요. 하지만 back up은 이제 콘텐츠 작업을, 저는 사이트용 그래픽 작업을 하고 있어요
20:09:15 &lt;zzz&gt; 웹사이트 자체를 넘어선 ‘캠페인’은 어떻게 하나요?
20:09:30 &lt;zzz&gt; 무엇을 계획하고 있죠? 그리고 언제?
20:09:34 &lt;eche|on&gt; 좋다
20:09:47 &lt;sadie_i2p&gt; 사이트에 새 페이지를 준비하고, 소셜 미디어 등을 통해 사람들을 그쪽으로 유도할 거예요...
20:10:00 &lt;sadie_i2p&gt; 새 스티커를 인센티브로 쓸 수도 있어요
20:10:10 &lt;eche|on&gt; 스티커!
20:10:17 &lt;zzz&gt; 오 좋네요, reseeder들에게 스티커, 훌륭한 아이디어예요
20:10:19 &lt;str4d&gt; 이게 'reseed가 무엇인가' 페이지인가요, 아니면 'reseed 운영 방법' 가이드인가요?
20:10:49 &lt;sadie_i2p&gt; 새로운 'reseed 운영 방법' 가이드예요
20:11:36 &lt;zzz&gt; sadie_i2p, 다음 마일스톤을 알려줄 수 있나요? (날짜, 내용)
20:12:12 &lt;str4d&gt; 그렇다면 개발자보다는 I2P의 '사용자'나 기여자를 위한 가이드가 되겠군요
20:12:26 &lt;str4d&gt; 이 가이드를 올릴 더 좋은 위치를 생각해보겠습니다
20:13:07 &lt;sadie_i2p&gt; 이건 좀 더 오래 걸릴 수 있어요 - 늦어도 두 달 내로 하겠습니다
20:13:10 &lt;str4d&gt; 음, 그런데...
20:13:21 &lt;sadie_i2p&gt; 가이드는 사용자와 기여자를 위한 것입니다
20:13:45 &lt;zzz&gt; sadie_i2p, 다음 달을 위한 중간 마일스톤도 주세요
20:13:59 &lt;sadie_i2p&gt; 아마 한 달 내로 콘텐츠 업데이트를 제공할 수 있어요
20:14:02 &lt;str4d&gt; 사실 'Get involved -&gt; Guides' 아래가 맞는 것 같네요
20:14:11 &lt;zzz&gt; ok great
20:14:16 &lt;zzz&gt; 넘어가죠
20:14:26 &lt;zzz&gt; str4d, gravy, cacapo: 사용 사례 추가, 우리가 무엇에 강한지, 더 많은 "passion"과 "fat", Bote 추가/강조, 완료 시점은
20:14:39 &lt;zzz&gt; 1월 OPEN, 새 날짜는 3월 1일
20:14:50 &lt;zzz&gt; cacapo가 좋은 사용 사례를 몇 개 작성한 걸 봤어요
20:15:06 &lt;str4d&gt; 응, dymaxion의 예시를 바탕으로 했어
20:15:11 &lt;zzz&gt; str4d, 그걸 'passion'과 'fat'을 좀 보태서 웹사이트에 반영하는 진행 상황은 어떤가요?
20:15:21 &lt;Yankee&gt; 신사 숙녀 여러분, 안녕하세요!
20:15:35 &lt;str4d&gt; 제 생각에는, 내용이 조금 다듬어져야 해요(약간 'I2P가 전부 해결!' 같은 느낌이 들어요)
20:16:03 &lt;str4d&gt; 사이트에서 위치는 아직 어디에 넣어야 할지 확신이 없어요
20:16:05 &lt;zzz&gt; str4d, 마감이 3월 1일이었는데, 이걸 웹사이트에 올릴 새 날짜를 줄 수 있나요?
20:16:45 &lt;str4d&gt; 이 항목의 '목표'는 첫 페이지 가운데 열과 지원 애플리케이션 페이지를 현재보다 더 좋게 만드는 것이었어요
20:18:02 &lt;str4d&gt; zzz, 제가 페이지를 URL로 올릴 수 있어요
20:18:42 &lt;zzz&gt; 이 작업 항목이 무엇인지에 대해 당신과 sadie_i2p가 같은 이해를 하고 있나요? sadie가 ccc에서 이것을 할 일 목록에 추가했어요
20:20:29 &lt;str4d&gt; 이건
20:20:45 &lt;str4d&gt; 시작일 뿐이고, 우리는 더 넓은 정보 구조를 여전히 정해야 해요
20:20:57 &lt;str4d&gt; 홈페이지로 실제로 무엇을 전달하려는지
20:21:42 &lt;zzz&gt; 좋아요, 그럼 첫 부분의 날짜를 주세요
20:21:49 &lt;zzz&gt; 부탁해요
20:22:12 &lt;str4d&gt; 이번 주 말까지 사용 사례 문서를 웹사이트로 이전하겠습니다
20:22:42 &lt;str4d&gt; 그리고 다음 회의에서 홈페이지 재구성에 대한 추가 진행 보고를 하겠습니다
20:23:04 &lt;zzz&gt; 좋아요, 훌륭합니다. 당신과 sadie가 'fat'과 'passion'이라는 더 큰 목표의 세부 사항을 논의하길 바랍니다.
20:23:39 &lt;zzz&gt; comraden이 I2P 스토리를 2월 말까지 편집/다듬기/개선/게시
20:24:13 &lt;zzz&gt; comraden1의 근황 아는 사람? 그의 편집된 초안을 돌려받아야 하고, 그 다음 제가 한 번 더 손보고 싶어요
20:25:00 &lt;zzz&gt; 이건 월요일에 웹사이트에 올라갔어야 했어요
20:25:30 &lt;sadie_i2p&gt; 새 날짜는 4월 1일 
20:25:59 &lt;zzz&gt; 좋아요. 그렇다면 몇 주 안에 그에게서 초안을 돌려받아야 해요
20:26:14 &lt;anonimal&gt; zzz: 현재 스토리 초안 링크?
20:26:39 &lt;zzz&gt; zzzi2p에 있는 것이 아직 최신이에요. comraden1이 "마스터"를 가지고 있는 동안에는 아무 변경도 하고 싶지 않아요
20:26:53 &lt;zzz&gt; 좋아요, 넘어가죠
20:27:09 &lt;zzz&gt; 티켓: Sadie가 검토하고, 권고안을 만들거나, 가능하면 관리를 시작 (기한은?) OPEN - 새 날짜 2월 중순(?)
20:27:09 &lt;anonimal&gt; 좋아요.
20:27:30 &lt;zzz&gt; sadie_i2p, 이 큰 작업은 어떻게 되어가나요?
20:28:06 &lt;sadie_i2p&gt; 어휴
20:29:12 &lt;zzz&gt; 어휴만으로는 좀 부족해요 :)
20:29:14 &lt;str4d&gt; 꽤 큰 작업이었죠 :P
20:29:35 &lt;sadie_i2p&gt; str4d와 주간 티켓 미팅에 대해 얘기했어요
20:29:56 &lt;zzz&gt; 그게 일회성 '검토'보다 더 현실적일 수 있겠네요
20:30:06 &lt;str4d&gt; 이걸 이전 회의에서 언급했던 것 같은데, 혹시 아니었다면: Trac에 "open" 상태를 추가했어요. 개발자가 확인했지만 담당자나 특별한 상태가 없는 티켓을 나타내기 위해서요.
20:30:26 &lt;str4d&gt; 그 목적은 그런 티켓을 실제로 '새로' 생성된 티켓과 구분하는 것이었어요
20:30:26 &lt;str4d&gt; 네, 그럴 거예요
20:30:26 &lt;zzz&gt; sadie_i2p, 티켓 관리를 어떻게 할지에 대해 권고안을 제시할 만큼 충분히 파악했나요?
20:31:08 &lt;str4d&gt; 그래서 우리가 스스로 만든 티켓들을 다른 상태로 옮긴 덕분에 'new' 티켓 더미가 이제 훨씬 작아졌어요
20:31:15 &lt;sadie_i2p&gt; 지금으로선 주간 체크인과 트리아지(triage)가 최선의 제안이에요
20:32:34 &lt;str4d&gt; +1
20:32:34 &lt;zzz&gt; 좋아요. 첫 미팅 일정을 잡을 준비가 되었나요, 아니면 먼저 더 정리할 게 있나요?
20:33:28 &lt;str4d&gt; 아직 여행 중이라 다음 주까지 기다리면 좋겠어요
20:33:46 &lt;zzz&gt; 좋아요. 4월 회의 전까지 아무 일정도 잡지 못하면, 그때 다시 호출하겠습니다
20:34:05 &lt;zzz&gt; str4d Android 0.9.24 릴리스를 2월 7일까지, TODO 목록 취합을 2월 26일까지
20:34:21 &lt;zzz&gt; 그건 조금 밀린 것 같네요 :)
20:34:28 &lt;str4d&gt; ㅎㅎ
20:34:34 &lt;zzz&gt; 새 날짜는?
20:34:37 &lt;str4d&gt; 둘 다 처참히 실패했어요, 박사 논문 때문에요
20:34:55 &lt;str4d&gt; (그걸 제가 드디어 2월 중순에 제출했습니다)
20:35:04 &lt;str4d&gt; 지금 이 순간 0.9.24 릴리스를 만들고 있어요
20:35:06 &lt;zzz&gt; 우와.
20:35:10 &lt;str4d&gt; (아주아주 느린 노트북에서()
20:35:14 &lt;str4d&gt; )
20:35:16 &lt;zzz&gt; 그리고 TODO 목록은요?
20:35:31 &lt;str4d&gt; TODO 목록 취합은 며칠 안에 하겠습니다
20:35:41 &lt;zzz&gt; 좋아요, 그 약속 지키도록 할게요
20:35:51 &lt;str4d&gt; ㅎㅎ :P
20:36:01 &lt;zzz&gt; str4d와 zzz가 2월 12일까지 VRP 티켓을 검토하기로. 저는 제 부분은 했어요.
20:36:06 &lt;str4d&gt; 주로 저장소 내 TODO 목록을 훑으며 제 개인 TODO 목록에 빠진 것을 찾는 일이에요
20:36:14 &lt;zzz&gt; 그건 새 날짜가?
20:36:20 &lt;anonimal&gt; Re: #1119, 3주 전에 zzz가 남긴 최신 댓글을 이제야 봤습니다. @mail.i2p/@i2pmail.org로 지난 몇 주 동안 github이나 다른 곳에서 이메일을 전혀 받지 못했습니다.
20:36:32 &lt;anonimal&gt; postman의 이메일 서비스에 문제가 있는지 진지하게 의심됩니다.
20:36:37 &lt;str4d&gt; 또 다른 논문 탓이죠. 0.9.24가 나가고 오늘 오후에 읽어보겠습니다
20:36:46 &lt;anonimal&gt; 이메일을 바꿔야 할지도 :/
20:36:49 &lt;zzz&gt; 좋아요, 훌륭해요
20:36:49 &lt;str4d&gt; anonimal, 응, 나도 최근에 심각한 문제가 있었어(이메일이 많이 반송됨)
20:37:03 &lt;zzz&gt; 믿거나 말거나, 1)은 이게 전부인 것 같네요
20:37:11 &lt;zzz&gt; 그리고 2)도
20:37:17 &lt;str4d&gt; (대략 2월 6일쯤부터)
20:37:22 &lt;anonimal&gt; zzz: 당신의 댓글을 더 깊이 읽고 VRP를 다시 쓰겠습니다.
20:37:28 &lt;zzz&gt; 3) 로드맵 미팅 준비 및 일정 http://zzz.i2p/topics/2021
20:37:33 &lt;anonimal&gt; 잠깐!
20:37:45 &lt;zzz&gt; 알았어요, 미안. 1이나 2에 대해 더 있을까요?
20:37:45 &lt;anonimal&gt; 1) 관련: H1 결정?
20:38:06 &lt;anonimal&gt; 내 기억으로 H1에 대한 결정은 1)로 옮겼던 것 같아요.
20:38:41 &lt;anonimal&gt; 아니면 말고요, 어쨌든 오늘 다룰 것 같아요.
20:38:47 &lt;zzz&gt; 지난 회의에서, VRP와 h1 논의를 3월 4~6일의 로드맵 미팅에서 마무리하기로 했어요
20:39:11 &lt;anonimal&gt; 알겠어요.
20:39:23 &lt;zzz&gt; 방금 일정을 잡았고, 내일과 일요일 UTC 오후 3시에 하겠습니다. anonimal, 둘 중 하나 참석할 수 있나요?
20:39:30 &lt;str4d&gt; 우와, 그러면 제가 검토할 기회가 생기네요 :P
20:41:08 &lt;zzz&gt; 그러면 3)으로 넘어가죠
20:41:11 &lt;zzz&gt; 말했듯이
20:41:19 &lt;zzz&gt; 방금 일정을 잡았고, 내일과 일요일 UTC 오후 3시에 하겠습니다. 
20:41:21 &lt;anonimal&gt; zzz: 으악, 토요일은 kovri의 최소 두 시간짜리 UTC 오후 6시 회의가 있어요.
20:41:21 * anonimal 생각 중
20:41:23 &lt;anonimal&gt; zzz: 토요일 회의는 얼마나 길어질 것 같나요?
20:41:33 &lt;orignal_&gt; 여기 있는 모두가 kovri 미팅을 신경 써야 하나요?
20:41:40 &lt;zzz&gt; 우리 미팅은 금요일과 일요일입니다. 토요일은 아니에요.
20:41:46 &lt;orignal_&gt; 그건 개인적으로 정리할 수 있지 않나요?
20:42:05 &lt;zzz&gt; 일요일 미팅에서 VRP를 가장 먼저 다루자고 제안합니다. 괜찮죠?
20:42:06 * anonimal 날짜를 헷갈림
20:42:11 &lt;anonimal&gt; 일요일은 가능해요.
20:42:16 &lt;anonimal&gt; 좋아요, 아주 좋네요.
20:43:00 &lt;zzz&gt; 이건 비공식적 미팅으로, 우리의 현재 위치와 앞으로의 방향을 검토할 거예요
20:43:11 &lt;zzz&gt; 목표는 적어도 올해 남은 기간의 로드맵을 정하는 것입니다
20:43:22 &lt;zzz&gt; 두 번째 미팅은 더 구조화될 수 있어요
20:43:46 &lt;zzz&gt; 다음에 무엇을 해야 할지, 그리고 올해 내내 무엇을 해야 할지 좀 막혔어요. 그래서 이 미팅은 제게 매우 중요하\
20:43:52 &lt;zzz&gt; 저의 방향을 설정하는 데
20:44:08 &lt;str4d&gt; 음음
20:44:15 &lt;anonimal&gt; 알겠어요.
20:44:37 &lt;zzz&gt; 그래서 금요일은 우선순위에 대한 좀 더 비공식적인 검토가 될 겁니다. 일요일에는 h1/vrp로 시작하고, 그 다음 .26~.29에 대한 로드맵을 확실히 정하겠습니다
20:44:47 &lt;zzz&gt; 3)에 관해 더 있을까요
20:45:31 &lt;zzz&gt; 4)로 넘어가죠
20:45:39 &lt;zzz&gt; 4) 행동 강령(Code of Conduct) 제안 (Sadie) http://zzz.i2p/topics/2015?page=2
20:45:56 &lt;zzz&gt; 지금 보니 debian과 비슷한 것을 하자고 제안했네요
20:46:00 &lt;zzz&gt; 아, 딱 맞게 돌아왔네요
20:46:12 &lt;zzz&gt; debian CoC에 대한 의견 있나요?
20:46:48 &lt;orignal_&gt; dedian은 익명 네트워크가 아닙니다
20:46:56 * str4d 링크를 연다
20:47:05 &lt;str4d&gt; orignal_, 아니지만, FOSS이긴 하죠
20:47:08 &lt;zzz&gt; 하지만 그들의 CoC에 대한 당신의 생각은 어떤가요, orignal_ ?
20:47:17 &lt;orignal_&gt; 사람들은 다양한 이유로 I2P에 옵니다
20:47:33 &lt;anonimal&gt; 제 생각엔 조금 미약하고, 어떻게 집행되는지 잘 모르겠습니다.
20:48:02 &lt;orignal_&gt; zzz, 그들의 CoC는 역사 있는 확립된 프로젝트인 그들에게는 적절해요
20:48:04 &lt;zzz&gt; sadie, debian CoC의 어떤 점이 마음에 드나요?
20:48:14 &lt;orignal_&gt; I2P는 전혀 다릅니다
20:48:32 &lt;sadie_i2p&gt; 최소한 시작하기 좋은 기본 구조를 제공하는 것처럼 보였어요
20:48:40 &lt;str4d&gt; orignal_, 그럼 I2P의&gt;10년이 넘는 역사도 확립된 프로젝트로 보지 않나요?
20:48:45 &lt;zzz&gt; 물론 우리는 다르지만, 우리는 분명히 역사 있는 확립된 프로젝트예요
20:48:51 &lt;orignal_&gt; 사람들이 여기 와서 다시 이런 HR의 헛소리를 듣는 건 정말 원하는 마지막 일일 거예요
20:49:31 &lt;zzz&gt; 사람들이 프로젝트에 오는 이유가 여기 와서 어떻게 행동해야 하는지에 대한 기준과 무슨 상관이 있는지 모르겠네요
20:49:41 &lt;zzz&gt; HR?
20:50:31 &lt;sadie_i2p&gt; 간단하고 요점을 찌르는 예시를 찾고 있어요 - 
20:50:31 &lt;sadie_i2p&gt; 그래서 아마 최선은 아니지만, 출발점으로는 괜찮을 거예요
20:51:29 &lt;zzz&gt; 출발점으로 debian이 더 낫다고 생각하나요, 아니면 monero가 더 나을까요
20:51:36 &lt;orignal_&gt; str4d, 안타깝게도 아니에요
20:51:51 &lt;str4d&gt; orignal_, “사용자 != 개발자”라는 점, 다시 한번요.
20:51:53 &lt;orignal_&gt; Debian과 I2P를 사용하는 사람 수를 비교해보세요
20:52:11 &lt;orignal_&gt; 큰 프로젝트를 그대로 따라 하려 하지 마세요, 우리는 아직 그 리그가 아니에요
20:52:12 &lt;str4d&gt; 사용자와 개발자를 혼동해선 안 됩니다.
20:52:21 &lt;zzz&gt; 우리 목표에 가장 가까운 것을 고를 수 있다면, 몇 사람이 우리 상황에 맞게 편집 작업을 하도록 부탁할 수 있다고 생각해요
20:52:42 &lt;str4d&gt; 그건 'Debian OS를 설치한 누구든 우리가 마음에 들어하지 않는 말을 해서는 안 된다'라고 말하는 것과 같을 거예요
20:52:42 &lt;str4d&gt; 그건 여기서의 요점이 전혀 아닙니다
20:52:53 &lt;str4d&gt; 따라서 사용자 기반 규모는 이 논의에서 중요하지 않습니다
20:52:54 &lt;sadie_i2p&gt; monero 것도 매우 좋아요 - 둘 중 그게 더 낫다면 이의 없습니다
20:53:21 &lt;orignal_&gt; zzz, CoC는 HR의 일이에요
20:53:21 &lt;orignal_&gt; 그 이상도 이하도 아니죠
20:53:28 &lt;zzz&gt; debian 대 monero에 대한 다른 분들의 의견은요?
20:53:44 &lt;anonimal&gt; + Monero
20:53:49 &lt;zzz&gt; orignal_, 'HR'이 무슨 뜻인가요?
20:54:07 &lt;orignal_&gt; HR = human resource(인사)
20:54:24 &lt;zzz&gt; monero 것이 debian보다 더 짧으니, 작게 시작하기는 더 쉬울 것 같네요
20:55:13 &lt;zzz&gt; monero CoC에 수정 제안을 표시해서 다음 달에 가져올 자원봉사자가 있나요?
20:55:18 &lt;str4d&gt; zzz, 저는 Debian 것의 핵심이 좋아요. 우리가 중요하게 여기는 많은 점을 다루고 있다고 생각하거든요(예: 최근에 항목 2가 매우 유용했을 겁니다)
20:55:26 &lt;zzz&gt; 아니면 debian 것도요
20:55:28 &lt;orignal_&gt; 제 의견을 다시 말하자면, 아직 그럴 때가 아니에요
20:55:40 &lt;zzz&gt; 지금 당장 debian 대 monero를 결정할 필요는 없어요
20:55:48 &lt;zzz&gt; orignal_, 당신의 메시지는 분명히 잘 전달되었습니다, 고마워요
20:55:59 &lt;str4d&gt; 그리고 지나치게 규정적이지도 않아요
20:56:13 &lt;zzz&gt; 아직 결정된 것은 없습니다. 그냥 논의 중이에요.
20:56:40 &lt;sadie_i2p&gt; 둘에서 가장 적용 가능한 것을 취할 수 있어요
20:56:43 &lt;anonimal&gt; CoC 관련,
20:56:56 &lt;str4d&gt; 또 제가 좋아하는 건 항목 6이에요 - 이슈에 응답할 때, 응답자 또한 CoC를 존중해야 한다는 점
20:57:03 &lt;anonimal&gt; https://github.com/monero-project/kovri/blob/master/doc/CONTRIBUTING.md
20:57:09 &lt;anonimal&gt; 아름다운 Monero 거버넌스 프로세스 그래픽도 포함되어 있어요.
20:57:30 &lt;comraden1&gt; zzz: 초안 관련 -- 회사 일이 더 복잡해졌고, 다시 관해(remission)에 들어간 가족 구성원을 돌보느라 역사 초안은 뒷전으로 미뤄졌습니다. sadie_i2p가 새 날짜로 2016-04-01을 언급했는데 그 기한을 지키도록 하겠습니다
20:57:30 &lt;str4d&gt; 오, 그림!
20:57:48 &lt;comraden1&gt; zzz: 몇 주 동안 소식이 뜸했던 점 사과드립니다!
20:58:06 &lt;anonimal&gt; str4d zzz: 네, 그리고 Java I2P에 맞게 기여 가이드를 패치할 의사가 있습니다.
20:58:52 &lt;anonimal&gt; 안녕 comraden1, 검토를 위해 story of i2p 페이지에 무언가를 올리고 있어요.
20:59:30 &lt;sadie_i2p&gt; 제가 자원할게요
20:59:58 &lt;comraden1&gt; anonimal: 고마워요 :) 포럼에 있으면 다음에 접속할 때 확인할게요. 제게 쪽지로 보내도 되고 clearnet으로 연락해도 돼요
21:00:05 &lt;zzz&gt; 좋아요, 훌륭합니다. Sadie_i2p와 anonimal, 다음 달 회의에 권고안을 가져와 주시겠어요?
21:00:20 &lt;sadie_i2p&gt; 물론이죠
21:00:25 &lt;zzz&gt; comraden1, 업데이트 고맙고, 가족 문제는 유감입니다
21:00:31 &lt;zzz&gt; 4)에 대해 더 있을까요?
21:00:40 * zzz baffer를 데운다
21:00:48 &lt;zzz&gt; 회의에 대해 더 있을까요?
21:00:54 &lt;orignal_&gt; 네, 다른 누군가를 위해 CoC를 쓰는 게 더 나은 일인 듯하군요
21:01:13 &lt;anonimal&gt; 네, 그런데 요즘 i2pmail에 문제가 있어서, 가능하면 sadie_i2p와 IRC에서 대화해보는 게 좋겠습니다.
21:01:21 &lt;anonimal&gt; 아니요, 회의 관련해선 더 없습니다 zzz.
21:01:52 &lt;zzz&gt; orignal_, kovri에 대한 빈정거리는 댓글로 우리 회의를 방해하지 말아 주세요. 지난달에는 너무 도가 지나쳤고, 다시는 그렇게 두지 않겠다고 약속했습니다
21:02:07 &lt;orignal_&gt; 그랬나요?
21:02:41 * zzz 회의 종료를 위해 *bafs*
21:02:45 &lt;zzz&gt; 모두 감사합니다 </div>
