---
title: "I2P 개발자 회의 - 2017년 2월 7일"
date: 2017-02-07
author: "zzz"
description: "2017년 2월 7일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> echelon, EinMbyte, manas, psi, str4d, zzz</p>

## 회의 로그

<div class="irc-log">20:00:00 &lt;zzz&gt; 0) 안녕하세요
20:00:00 &lt;zzz&gt; 1) 33C3 후속 논의
20:00:00 &lt;zzz&gt; 2) 0.9.29 업데이트 (zzz)
20:00:00 &lt;zzz&gt; 3) Tails 유지관리자 (zzz) http://zzz.i2p/topics/2108
20:00:00 &lt;zzz&gt; 4) NTCP2 초안 (Manas)
20:00:00 &lt;zzz&gt; 5) Reseed(부트스트랩) 문서 패치 (Manas)
20:00:04 &lt;zzz&gt; 0) 안녕하세요
20:00:05 &lt;zzz&gt; 안녕
20:00:21 &lt;zzz&gt; 1) 33C3 후속 논의
20:00:32 &lt;eche|off&gt; 안녕
20:00:50 &lt;zzz&gt; 33c3에 대해 말하고 싶은 거 있나요? 우리 테이블 방문자는 예년보다 적었다고 하겠네요
20:01:07 &lt;zzz&gt; zzz.i2p에 글 몇 개 작성해준 manas에게 감사합니다
20:01:09 &lt;psi&gt; 오하이
20:01:15 &lt;eche|off&gt; 맞아요, 적긴 했지만 그래도 괜찮았어요
20:01:21 &lt;zzz&gt; 3)에서 Tails를 다루겠습니다
20:01:32 &lt;zzz&gt; 올해는 새로운 도시를 기대해봅시다
20:01:54 &lt;zzz&gt; 1)에 대해 더 있을까요?
20:02:25 &lt;i2pr&gt; [Slack/str4d] 안녕하세요
20:02:26 &lt;i2pr&gt; [Slack/str4d] 그건 코멘트하기 어렵지만, 정말 즐거웠어요!
20:02:28 &lt;manas&gt; 헤이!
20:02:38 &lt;zzz&gt; 좋아요, 넘어가죠
20:02:43 &lt;zzz&gt; 2) 0.9.29 업데이트 (zzz)
20:02:51 &lt;i2pr&gt; [Slack/str4d] Linz와 Vienna에서 Yolgie와 좋은 시간 보냈어요; 앞으로 좋은 협력으로 이어질 것 같아요
20:03:17 &lt;zzz&gt; 체크인 마감일을 지금부터 2주 반 뒤인 2/24 금요일로 잡았고, 릴리스는 2/27쯤으로요
20:03:21 &lt;zzz&gt; 대부분 버그 수정입니다
20:03:30 &lt;eche|off&gt; 어, 뭔가 할 시간입니다, 좋아요
20:03:40 &lt;zzz&gt; 또한 조만간 stats.i2p 등록에서 서명을 강제(여전히 계획 중)할 예정입니다
20:04:04 &lt;manas&gt; 서명을 강제요?
20:04:12 &lt;zzz&gt; str4d의 콘솔 개편은 .30으로 미뤄졌으니, prop(제안) 마감은 2월 중순이 되겠네요
20:04:17 &lt;zzz&gt; *3월 중순
20:04:32 &lt;manas&gt; 그럼 호스트 이름을 등록할 때 검증 단계가 더 생긴다는 건가요?
20:04:42 &lt;zzz&gt; manas, 기본적으로 등록하려는 도메인을 당신이 제어한다는 증명입니다
20:05:10 &lt;manas&gt; 흠, 알겠어요
20:05:15 &lt;zzz&gt; 주말 동안 버그 여러 개를 고치고 trac 티켓들을 처리했습니다. 앞으로 1~2주 동안 몇 개 더 시도할 거예요
20:05:38 &lt;zzz&gt; 그래서 태그 프리즈와 tx 푸시는 약 8일 후가 될 겁니다
20:06:07 &lt;zzz&gt; man 페이지 번역하는 방법을 알아냈으니, 모두 transifex에서 작업해 주세요
20:06:13 &lt;zzz&gt; 2)에 대해 더 있을까요?
20:06:16 &lt;i2pr&gt; [Slack/str4d] 우와
20:06:19 &lt;i2pr&gt; [Slack/str4d] .29를 위해 제가 할 만한 유용한 일이 있으면 알려주세요. 아니면 .ui 브랜치 작업을 계속할게요.
20:06:20 &lt;eche|off&gt; 이미 했어요^^
20:06:37 &lt;eche|off&gt; 내 reseed에 인증서를 설정할게요... 
20:06:45 &lt;manas&gt; 힌디어 번역 작업을 계속하고 있어요 :)
20:07:04 &lt;zzz&gt; 맞아요 str4d, prop하기 전에 확실히 손봐야 할 것들이 있어요, 아니면 사람들이 들고일어날 겁니다
20:07:14 &lt;zzz&gt; 좋아요, 훌륭해요
20:07:29 &lt;zzz&gt; 3) Tails 유지관리자 (zzz) http://zzz.i2p/topics/2108
20:07:40 &lt;i2pr&gt; [Slack/str4d] 푸시하기 전에 정리 중인 로컬 변경 사항이 여러 개 있어요
20:08:07 &lt;zzz&gt; ccc에서 'yolgie'라는 사람을 만났고, 그가 하겠다고 했어요. 1월 초에 연락했을 때 2월에 시작하겠다고 했고, 며칠 전에 다시 연락했지만 아직 응답이 없습니다
20:08:26 &lt;zzz&gt; 우리는 곧 Tails에서 퇴출될 지경이라, 도와줄 수 있는 사람 누구든 환영합니다
20:08:45 &lt;psi&gt; 언제든 Tails로 갈 준비가 되어 있어요. 마침내 Tails 빌드를 완전히 익혔습니다
20:08:51 &lt;i2pr&gt; [Slack/str4d] 그건 일정이 어떻게 되나요?
20:08:57 &lt;manas&gt; psi: 멋져요!
20:09:50 &lt;zzz&gt; 우리 퇴출 일정이 적힌 Tails 티켓 링크는 zzz.i2p 스레드를 보세요
20:09:55 &lt;zzz&gt; *eviction
20:11:15 &lt;zzz&gt; 오래된 티켓들도 많고 비판하는 사람들도 많아서, 사실상 거의 끝난 셈입니다
20:11:20 &lt;zzz&gt; 3)에 대해 더 있을까요?
20:11:44 &lt;eche|off&gt; 잘 되길 바랍니다
20:11:55 &lt;zzz&gt; 4) NTCP2 초안 (Manas)
20:12:00 &lt;zzz&gt; manas, 준비한 게 무엇이 있나요?
20:12:24 &lt;manas&gt; 초안을 준비했고, zzz.i2p에 올려두었습니다
20:12:40 &lt;manas&gt; 오늘까지는 코멘트를 못 들었습니다
20:12:51 &lt;zzz&gt; 그럼 예전 제안과 EinMByte의 완전한 재작성본을 합친 건가요?
20:13:07 &lt;manas&gt; 중요한 부분들은 포함했다고 생각하지만, 이 주제를 더 잘 아는 분의 검토가 필요합니다.
20:13:14 &lt;eche|off&gt; 언제 끝나냐고 묻는 사람들은 있지만, 그뿐이에요..
20:13:30 &lt;manas&gt; zzz: 네
20:13:47 * psi가 ntcp 제안을 읽기 시작한다
20:13:53 &lt;zzz&gt; 작지만 진전입니다. 그래도 전체적으로는 완전히 정체되어 있다고 보고, 사람들이 참여하기 전까지는 진척이 없을 겁니다
20:14:00 &lt;manas&gt; zzz: 오래되어 시대에 뒤떨어진 예전 제안의 부분들은 포함하지 않았습니다
20:14:22 &lt;zzz&gt; 좋아요, 며칠 더 두겠습니다. zzz.i2p 스레드에 코멘트가 없으면 웹사이트에 그냥 체크인할까요?
20:14:59 &lt;manas&gt; zzz: (스타일)과 같은 사소한 편집 몇 가지는 마지막에 할 수 있어요
20:15:09 &lt;zzz&gt; 좋아요, 훌륭합니다. 4)에 대해 더 있을까요?
20:15:16 &lt;manas&gt; tuna의 최근 글에서
20:15:38 &lt;manas&gt; 하지만 그게 전부입니다
20:15:41 &lt;zzz&gt; 5) Reseed 문서 패치 (Manas)
20:15:46 &lt;zzz&gt; manas, 준비한 게 무엇이 있나요?
20:16:04 &lt;manas&gt; backup에게서 소식을 들었습니다
20:16:08 &lt;manas&gt; 그의 코멘트는 여기 있습니다: http://zzz.i2p/topics/2210-reseed-webpage-updates
20:16:27 &lt;manas&gt; 그의 제안을 반영한 후에 또 다른 패치를 만들겠습니다
20:16:46 &lt;eche|off&gt; 좋네요
20:16:48 &lt;manas&gt; 그가 여러 부분(오래된 Reseed 방법들)을 제거하자고 제안했습니다
20:16:56 &lt;manas&gt; 또한 lighttpd 지원을 제거하자는 제안도 했습니다
20:17:06 &lt;eche|off&gt; 저는 여전히 예전 방법을 쓰지만, 괜찮아요
20:17:09 &lt;manas&gt; Reseed를 돌리는 데 lighttpd를 누가, 혹은 누가라도 쓰고 있는지 모르겠어요
20:17:26 &lt;zzz&gt; 훌륭한 작업입니다. backup이 그 페이지의 소유자이지만 자신의 변경사항에 대해 html 패치를 만들길 거부하고, 저도 html 편집자가 되길 거부해서 1년 동안 막혀 있었죠. 우리를 앞으로 나아가게 해줘서 고맙습니다.
20:17:29 &lt;manas&gt; 특정 HTTP 헤더를 설정할 수 없는 이슈가 있습니다
20:17:55 &lt;manas&gt; :)
20:18:10 &lt;zzz&gt; manas, 이건 완료되면 zzz.i2p 스레드에 메모를 추가해 주세요. 제가 체크인하겠습니다
20:18:44 &lt;manas&gt; backup이 제안한 변경사항에 대해 누구든 의견이 있으면 올려 주세요. 일주일 내에 의견이 없으면 업데이트된 패치를 공유하고 zzz에게 알리겠습니다.
20:18:57 &lt;zzz&gt; 5)에 대해 더 있을까요?
20:18:59 &lt;manas&gt; zzz: 네
20:19:16 &lt;manas&gt; 제 쪽에서는 없습니다
20:20:03 &lt;zzz&gt; 회의에 대해 더 있을까요?
20:20:21 &lt;eche|off&gt; 제 쪽에서는 없어요
20:20:28 &lt;EinMByte&gt; 늦었네요, 그런데 ntcp2에 관해
20:20:39 &lt;manas&gt; 안녕하세요 EinMByte 
20:20:40 &lt;zzz&gt; 말씀하세요
20:21:00 &lt;EinMByte&gt; 최신 초안을 검토하겠습니다
20:21:24 &lt;EinMByte&gt; 어떤 암호 알고리즘을 지원할지에 대해 결정이 내려졌나요?
20:21:27 &lt;manas&gt; 참고로 여기에 있어요: http://pinkpaste.i2p/show/246/
20:21:39 &lt;psi&gt; 거기 있네요
20:22:19 &lt;zzz&gt; 기본적으로 1MB 초안 이후로 진전이 없었고, 방금 manas가 그것을 이전 제안과 병합했습니다
20:22:28 &lt;zzz&gt; 회의에 대해 더 있을까요?
20:22:58 &lt;EinMByte&gt; 좋아요, 초안을 읽겠습니다. 누군가 Winter에게 연락해야 합니다
20:23:04 &lt;EinMByte&gt; (아마 제가요)
20:23:11 * zzz가 baffer를 잡는다
20:23:24 * zzz가 회의를 종료하며 *bafs* </div>
