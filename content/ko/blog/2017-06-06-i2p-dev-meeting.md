---
title: "I2P 개발자 회의 - 2017년 6월 6일"
date: 2017-06-06
author: "zzz"
description: "2017년 6월 6일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단 요약

<p class="attendees-inline"><strong>참석자:</strong> backup, lazygravy, manas, psi, str4d, zzz</p>

## 회의 로그

<div class="irc-log">20:00:18 &lt;zzz&gt; 0) 안녕하세요
20:00:18 &lt;zzz&gt; 1) 0.9.31 업데이트 (zzz)
20:00:18 &lt;zzz&gt; 2) UI 브랜치 상태 - (str4d)
20:00:18 &lt;zzz&gt; 3) I2P Summer Dev 계획 - (str4d)
20:00:18 &lt;zzz&gt; 4) EdDSA 업데이트 - (str4d)
20:00:18 &lt;zzz&gt; 5) 34C3 계획 (zzz/echelon)
20:00:18 &lt;zzz&gt; 6) 정기 Reseed 운영자 회의 (manas)
20:00:24 &lt;zzz&gt; 0) 안녕하세요
20:00:26 &lt;manas&gt; 안녕하세요 :)
20:00:26 &lt;zzz&gt; 하이
20:00:34 &lt;psi&gt; 오하이
20:00:40 &lt;i2pr&gt; [Slack/str4d] 안녕하세요
20:00:58 &lt;zzz&gt; 1) 0.9.31 업데이트 (zzz)
20:01:00 &lt;backup&gt; 안녕하세요
20:01:37 &lt;zzz&gt; 좋아, 체크인 마감이 3주 반 뒤고, 일정은 잘 맞고 있음. 하지만 31 로드맵의 대부분(29, 30에서 미뤄진 것들)은 다시 미뤄질 예정
20:01:54 &lt;zzz&gt; 태그 동결은 어제였음
20:02:03 &lt;zzz&gt; 1)에 대해 더 있나요?
20:02:23 &lt;backup&gt; 오늘 리시드 업데이트 몇 가지를 보냈어요
20:02:26 &lt;psi&gt; .31에서 i2pd에 주목할 만한 변경 사항 있나요?
20:03:01 &lt;zzz&gt; i2pd 쪽은 잘 모르겠는데, i2np 변경은 없음
20:03:15 &lt;zzz&gt; 31의 대부분은 UI 관련 내용일 거임 (항목 2 참고)
20:03:21 &lt;zzz&gt; 1)에 대해 더 있나요?
20:03:51 &lt;psi&gt; ㅇㅋ
20:03:51 &lt;i2pr&gt; [Slack/str4d] 새 웹사이트 프론트 페이지 CSS도 같은 시기에 반영될 예정
20:04:07 &lt;manas&gt; str4d: 굿
20:04:28 &lt;zzz&gt; 2) UI 브랜치 상태 - (str4d)
20:04:31 &lt;zzz&gt; str4d 진행
20:04:33 &lt;i2pr&gt; [Slack/str4d] (그리고 가능하면 내부 CSS도 일부, 다만 Elio 일정에 달림)
20:04:55 &lt;i2pr&gt; [Slack/str4d] UI 브랜치가 머지됨!
20:05:36 &lt;i2pr&gt; [Slack/str4d] 몇 분이 리뷰하고 피드백 주셨음; 감사
20:05:39 &lt;zzz&gt; 모두 테스트해보고, 이슈든 비이슈든 ticket #1996에 추가해 주세요
20:05:59 &lt;zzz&gt; str4d, 변경할 때는 rev(리비전)을 올려서 코멘트가 의미 있게 보이게 해줘
20:06:26 &lt;i2pr&gt; [Slack/str4d] ㅇㅋ
20:06:32 &lt;zzz&gt; 2)에 대해 더 있나요?
20:06:59 &lt;i2pr&gt; [Slack/str4d] 대부분의 버그는 처리했음; 시간 나면 주관적인 지적에도 답해볼게
20:07:42 &lt;zzz&gt; 3) I2P Summer Dev 계획 - (str4d)
20:07:46 &lt;zzz&gt; str4d 진행
20:08:14 &lt;i2pr&gt; [Slack/str4d] 사이트 병합 이슈 때문에 Summer Dev가 하루 늦게 시작했지만, 지금 올라가 있음!
20:08:46 &lt;i2pr&gt; [Slack/str4d] 이제 재미있는 부분: 관련 작업 시작
20:09:32 &lt;i2pr&gt; [Slack/str4d] 제안된 아이디어 목록을 Dev 포럼에 올려서 사람들이 볼 수 있게 할게
20:09:39 &lt;zzz&gt; 그 주제로 벌써 회의 두 번 했던 걸로 아는데...
20:09:57 &lt;manas&gt; Tor 위에서 병렬 rsync 전송을 하는 스크립트가 있는데, I2P 위에서 전송되도록 손볼 생각이었어요 :)
20:09:58 &lt;i2pr&gt; [Slack/str4d] 하나는 했고, 지난주 건에는 아무도 안 왔어요
20:10:02 &lt;zzz&gt; 도움을 받을 수 있는 일로는 무엇을 생각하고 있어?
20:10:35 &lt;zzz&gt; 그리고 PR 계획은?
20:11:32 &lt;i2pr&gt; [Slack/str4d] PR 계획은 격주로 Summer Dev의 한 측면에 관한 새 블로그 글을 내는 것
20:11:44 &lt;i2pr&gt; [Slack/str4d] 하지만 실제로 작업이 진행되는지에 크게 좌우됨
20:12:07 &lt;i2pr&gt; [Slack/str4d] 메트릭 수집이 가장 큰 과제
20:12:36 &lt;manas&gt; 첫 회의 기록을 읽었는데, 지금으로선 제가 잘 모르는 기술적인 내용 같더군요 :P
20:12:45 &lt;zzz&gt; 좋아. 3)에 대해 더 있나요?
20:13:12 &lt;i2pr&gt; [Slack/str4d] 핵심은 진척을 내는 것
20:13:24 &lt;manas&gt; 메트릭 수집이 좋겠어요. 목적지를 입력하면 메트릭을 수집하고/또는 속도 테스트를 실행하는 Java 플러그인 같은 것?
20:13:39 &lt;manas&gt; 그에 대해 원래 계획된 방향이 뭔지는 확실치 않아요
20:13:41 &lt;i2pr&gt; [Slack/str4d] 가능하죠, 네
20:13:50 &lt;manas&gt; 그거 멋지겠네요
20:14:02 &lt;i2pr&gt; [Slack/str4d] 제가 생각한 방향은 metrics.torproject.org 같은 것
20:14:21 &lt;i2pr&gt; [Slack/str4d] 물론 거기와 동일한 메트릭을 말하는 건 아님
20:14:30 &lt;manas&gt; 맞아요
20:14:41 &lt;i2pr&gt; [Slack/str4d] 하지만 우리도 비슷한 셋업
20:14:59 &lt;i2pr&gt; [Slack/str4d] 핵심 메트릭은 tunnel / 네트워크 성능
20:15:39 &lt;zzz&gt; 좋은 목표지만, Tor에서 쉬운 건 우리에겐 어렵지. 그쪽은 중앙집중식 제어가 있으니까
20:15:40 &lt;i2pr&gt; [Slack/str4d] 그래서 Tor가 bwauth(대역폭 권한자) 코드로 돌리는 테스트를 누가 한번 살펴보면 정말 도움이 될 거야
20:15:55 &lt;i2pr&gt; [Slack/str4d] 동의
20:16:02 &lt;manas&gt; 맞아요. Tor의 메트릭 수집에서 프라이버시를 지키는 관행을 어디선가 언급하셨던 것 같아요. 관련 문서/논문이 있으면 읽어보면 좋겠네요
20:16:06 &lt;i2pr&gt; [Slack/str4d] 하지만 메트릭은 본질적으로 중앙집중화될 수밖에 없음
20:16:34 &lt;i2pr&gt; [Slack/str4d] freehaven.net/anonbib에 몇 편의 논문이 있어요
20:16:45 &lt;zzz&gt; 3)에 대해 더 있나요?
20:16:54 &lt;manas&gt; 감사해요, 살펴볼게요
20:16:55 &lt;i2pr&gt; [Slack/str4d] 다만 그들의 구체적인 셋업에 대해 얼마나 다루는지는 확실치 않음
20:17:12 &lt;i2pr&gt; [Slack/str4d] 이번 달 다른 일은 proposal 작업
20:17:36 &lt;zzz&gt; 4) EdDSA 업데이트 - (str4d)
20:17:39 &lt;zzz&gt; str4d 진행
20:17:40 &lt;i2pr&gt; [Slack/str4d] 관련 있다고 생각한 proposal 몇 가지를 런치 블로그 글에 나열했음
20:17:48 &lt;i2pr&gt; [Slack/str4d] zzz, 너무 서두르지 마
20:17:57 &lt;i2pr&gt; [Slack/str4d] 지금 폰이라 타이핑이 빠르지 않음
20:18:20 &lt;i2pr&gt; [Slack/str4d] 3) 계속
20:18:53 &lt;i2pr&gt; [Slack/str4d] 이번 달 남은 기간은 proposal을 검토하고 작업할 예정
20:19:09 &lt;i2pr&gt; [Slack/str4d] 그중 몇 가지에 대해 블로그 글 한두 개는 나왔으면 해
20:19:18 &lt;zzz&gt; proposals가 3)인 Summer Dev와 어떻게 관련돼?
20:19:43 &lt;i2pr&gt; [Slack/str4d] Summer Dev는 속도에 관한 것
20:20:07 &lt;i2pr&gt; [Slack/str4d] 성능 관련으로 열린 proposal이 몇 개 있어
20:20:42 &lt;i2pr&gt; [Slack/str4d] 그중 일부가 더 넓은 커뮤니티에 전달되면 좋겠어
20:20:48 &lt;zzz&gt; 오케이
20:20:55 &lt;zzz&gt; 3)에 대해 더 있나요?
20:20:56 &lt;i2pr&gt; [Slack/str4d] 사실 신참이 하기 좋은 작업이야
20:21:12 &lt;i2pr&gt; [Slack/str4d] proposal을 시간을 들여 읽고
20:21:18 &lt;i2pr&gt; [Slack/str4d] 관련 문서도 읽고
20:21:28 &lt;i2pr&gt; [Slack/str4d] 그걸 블로그 글로 소화해서 정리
20:21:37 &lt;manas&gt; str4d: 작업이란 proposal을 읽고 이해한 다음, 블로그 글로 쉽게 풀어 설명하는 걸 말하나요?
20:21:44 &lt;manas&gt; 앗 지금 막 메시지가 들어왔네요, 랙
20:21:46 &lt;manas&gt; :)
20:21:49 &lt;i2pr&gt; [Slack/str4d] 맞아요!
20:21:54 &lt;manas&gt; 그 proposal들 살펴볼게요, str4d 
20:22:02 &lt;manas&gt; 재미있을 것 같아요
20:22:13 &lt;i2pr&gt; [Slack/str4d] proposal이 무엇이며, 성능과 프라이버시 양측에 왜 중요한지 전달
20:22:27 &lt;manas&gt; 네, 좋은 블로그 연재가 되겠네요 :)
20:22:37 &lt;manas&gt; 그리고 생산적인 논의도 이어지길
20:22:45 &lt;i2pr&gt; [Slack/str4d] 정확해 ;)
20:23:09 &lt;zzz&gt; 3)에 대해 더 있나요?
20:23:16 &lt;i2pr&gt; [Slack/str4d] 좋아, 이제 3) 끝
20:23:31 &lt;zzz&gt; 4) EdDSA 업데이트 - (str4d)
20:23:34 &lt;zzz&gt; str4d 진행
20:23:43 &lt;i2pr&gt; [Slack/str4d] 여긴 진전 없음
20:24:04 &lt;i2pr&gt; [Slack/str4d] 브랜치는 얼마 전에 제 라이브러리의 최신 코드로 업데이트해 둠
20:24:19 &lt;i2pr&gt; [Slack/str4d] 하지만 UI 때문에 리뷰할 시간이 없었음
20:24:27 &lt;zzz&gt; 다음 회의로 이월할까요, 아니면 이 항목은 끝났거나 관련 없나요?
20:25:07 &lt;i2pr&gt; [Slack/str4d] 주요 이슈는 sigtypes(서명 유형)의 의미적 변경이 예상치 못한 것을 깨뜨리지 않는지 확인하는 것
20:26:07 &lt;i2pr&gt; [Slack/str4d] 도와줄 사람이 있다면 좋겠지만, 우선순위는 Summer Dev를 더 높게 두겠음
20:26:32 &lt;i2pr&gt; [Slack/str4d] 그래서 당장은 'table' 하겠음
20:26:51 &lt;zzz&gt; 다음 회의로 이월할까요, 아니면 이 항목은 끝났거나 관련 없나요?
20:27:05 &lt;i2pr&gt; [Slack/str4d] 방금 말했어요
20:27:21 &lt;i2pr&gt; [Slack/str4d] 지금은 'table'. 그러니 끝난 것도 무관한 것도 아니고, 하지만 안건에서는 빼자
20:27:27 &lt;zzz&gt; ‘table’을 어떻게 해야 할지 모르겠네. 안건에 올릴까 말까?
20:27:53 &lt;zzz&gt; 좋아, 그럼 test2 브랜치는 태웠고, 브랜치 작업을 더 하게 되면 새로 만들게
20:28:02 &lt;zzz&gt; 좋아 4)에 대해 더 있나요?
20:29:01 &lt;zzz&gt; 5) 34C3 계획 (zzz/echelon)
20:29:25 &lt;zzz&gt; ech는 지금 없는 것 같아. 미리 알리면, 예산 회의는 다음 달이나 8월에 있을 거야
20:29:33 &lt;manas&gt; 알겠어요
20:29:56 &lt;i2pr&gt; [Slack/str4d] ACK
20:29:57 &lt;zzz&gt; 지급할 자금은 충분하지만, 늘 그렇듯 기여자에게 보상함
20:30:16 &lt;zzz&gt; 그러니 프로젝트를 도우면 프로젝트도 여러분을 도울 것
20:30:18 &lt;manas&gt; 항공편이랑 호텔을 알아보고 있었어요. 거의 정리했어요
20:30:21 &lt;zzz&gt; 지금이 적기
20:30:26 &lt;lazygravy&gt; (특히 btc 가격이 미쳐서)
20:30:36 &lt;zzz&gt; 자세한 건 다음 회의들에서
20:30:45 &lt;manas&gt; 호텔이 빨리 차는 것 같으니, 갈 계획이 있으면 최대한 빨리 알아보는 게 좋아요
20:30:52 &lt;zzz&gt; ㅇㅇ
20:30:57 &lt;zzz&gt; 5)에 대해 더 있나요?
20:31:03 &lt;i2pr&gt; [Slack/str4d] +1
20:32:01 &lt;zzz&gt; 6) 정기 Reseed 운영자 회의 (manas)
20:32:03 &lt;zzz&gt; manas 진행
20:32:26 &lt;manas&gt; http://zzz.i2p/topics/2341-meeting-reseed-operators-13-june-8-pm-utc-in-i2p-reseed - 다음 주 6월 13일 8PM UTC에 #i2p-reseed에서 첫 리시드 회의를 계획 중
20:32:46 &lt;manas&gt; 저게 일반적인 논의 포인트고, 언급한 스레드를 제가 요약할게요
20:32:59 &lt;manas&gt; 다음 주에 봬요, 감사합니다 :)
20:33:12 &lt;zzz&gt; 좋습니다, 준비해 줘서 고마워요, 모두 참석하길 권합니다
20:33:18 &lt;zzz&gt; 6)에 대해 더 있나요?
20:33:26 &lt;manas&gt; 이상입니다
20:34:21 &lt;lazygravy&gt; 3)으로 다시 돌아가도 무리 없을까요?
20:34:35 &lt;manas&gt; 무슨 일이야 gravy
20:34:45 &lt;lazygravy&gt; 수집 쪽에 관심 있어요, str4d. 이거에 대해 이야기할 시간을 잡을 수 있을까요? 주말이면 좋겠어요
20:34:47 &lt;zzz&gt; 3) gravy 진행
20:35:00 &lt;manas&gt; #i2p-science에서 논의해도 될까요?
20:35:45 &lt;lazygravy&gt; manas: 시간만 정해지면요 :)
20:36:01 &lt;lazygravy&gt; 지금 시간을 정할 필요는 없어요. 그냥 말만 꺼내두고 싶었어요
20:36:06 &lt;manas&gt; 네
20:36:48 &lt;manas&gt; 저도 흥미로울 것 같네요
20:37:01 &lt;zzz&gt; 3)에 대해 더 있나요?
20:37:43 &lt;lazygravy&gt; 저는 더 없어요
20:37:48 &lt;zzz&gt; 회의에서 더 다룰 거 있나요?
20:37:56 * zzz baffer를 찾는다
20:39:02 * zzz *b*a*f*s* 회의 종료 </div>
