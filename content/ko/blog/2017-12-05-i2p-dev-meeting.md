---
title: "I2P 개발자 회의 - 2017년 12월 5일"
date: 2017-12-05
author: "zzz"
description: "2017년 12월 5일자 I2P 개발 회의록"
categories: ["meeting"]
---

## 간단 요약

<p class="attendees-inline"><strong>참석자:</strong> str4d, orignal, zlatinb, zzz</p>

## 회의 기록

<div class="irc-log">20:00:00 &lt;zzz&gt; 0) 안녕하세요
20:00:00 &lt;zzz&gt; 1) 0.9.33 업데이트 (zzz)
20:00:00 &lt;zzz&gt; 2) 34C3 계획 (zzz)
20:00:03 &lt;zzz&gt; 0) 안녕하세요
20:00:05 &lt;zzz&gt; hi
20:00:30 &lt;zzz&gt; 1) 0.9.33 업데이트 (zzz)
20:00:48 &lt;zzz&gt; 0.9.33 개발은 지금까지 diff 2만 줄로 아주 힘차게 시작했습니다
20:00:55 &lt;zzz&gt; 좋은 수정 사항이 많이 들어갔습니다
20:01:17 &lt;zlatinb&gt; hi
20:01:42 &lt;zzz&gt; 그리고 0.9.32 Android는 2주 목표보다 늦어졌기 때문에, 데스크톱 릴리스 전에 Google Play 크래시를 검토하도록 프로세스를 일부 변경했습니다
20:02:01 &lt;i2pr&gt; [Slack/str4d] hi
20:02:02 &lt;zzz&gt; 이로 인해 Android 릴리스를 더 빠르고 품질 높게 할 수 있을 것입니다
20:02:29 &lt;i2pr&gt; [Slack/str4d] 로컬에 보관 중인 CSS와 JSP 패치가 더 있습니다. 이번 주말에 정리해서 mtn에 올려 더 길게 리뷰받고 싶습니다.
20:02:40 &lt;zzz&gt; 1월 말 0.9.33 릴리스 일정에 맞춰 진행 중이라고 생각합니다. 즉, 큰 변경 사항은 CCC 전에, 이번 달에 반영되어야 합니다
20:03:28 &lt;zzz&gt; 스트리밍 관련으로 더 손볼 것들이 있고, 이번 주에는 susimail 이슈를 수정하고 있습니다
20:04:12 &lt;zzz&gt; 1)에 대해 다른 내용 있나요?
20:04:24 &lt;zlatinb&gt; 가능하다면 postman의 트래커에 dev 빌드를 올리면 좋겠습니다
20:04:35 &lt;zlatinb&gt; 거기에 올라오는 건 뭐든지 받아서 써 보는 사람들이 있습니다
20:04:50 &lt;zzz&gt; bobthebuilder.com에서 마그넷 또는 토렌트 파일로 받을 수 있을 겁니다
20:05:17 &lt;zlatinb&gt; 아 맞아요, 다만 postman에 올라오면 노출이 훨씬 커집니다
20:05:43 &lt;zzz&gt; 좋아요, 그건 bobthebuilder 운영자에게 이야기해 보세요, 좋은 생각이네요
20:05:54 &lt;zzz&gt; 1)에 대해 다른 내용 있나요?
20:05:58 &lt;i2pr&gt; [Slack/str4d] 또한 이제 Travis CI에서 지속적 빌드도 하고 있으니, 다른 관점에서 보시려면 https://travis-ci.org/i2p/i2p.i2p 를 주시해 주세요
20:06:44 &lt;zzz&gt; str4d, 그걸 위한 IRC 봇을 설정해 줄 수 있으면 도움이 될 거예요, 웹사이트를 확인하는 걸 기억하기가 어렵거든요
20:07:17 &lt;zzz&gt; 1)에 대해 다른 내용 있나요?
20:08:01 &lt;zzz&gt; 2) 34C3 계획 (zzz)
20:08:10 &lt;zzz&gt; 좋아요, 스티커 관련 상황은 잘 관리되고 있습니다
20:08:25 &lt;zzz&gt; 기차표는 eche|on이 가지고 있습니다
20:08:33 &lt;zzz&gt; hottuna가 위키에 우리를 등록했습니다
20:08:43 &lt;zzz&gt; noisy square가 위키에 이미 나타났나요?
20:08:50 &lt;zzz&gt; 그리고 배너는 누가 가지고 있죠?
20:09:23 &lt;zzz&gt; 다른 누가 먼저 하지 않으면 나중에 트위터 DM 그룹을 만들겠습니다
20:11:01 &lt;zzz&gt; 아무 응답이 없네요... 2)에 대해 다른 내용 있나요?
20:12:01 &lt;zzz&gt; 회의에 대해 다른 내용 있나요?
20:12:33 &lt;orignal&gt; 회의를 덜 자주 여는 게 더 나을 수도 있겠네요?
20:12:47 &lt;orignal&gt; 관심이 부족해서요
20:12:56 &lt;orignal&gt; 하지만 더 홍보해야 해요
20:13:09 &lt;i2pr&gt; [Slack/str4d] 기대하고 있어요!
20:13:35 &lt;i2pr&gt; [Slack/str4d] 월 1회 정도가 적당하다고 생각합니다
20:13:41 &lt;zzz&gt; orignal, 그건 CCC에서 논의해도 되겠네요.
20:13:47 &lt;i2pr&gt; [Slack/str4d] 이 시간이 좋은지 여부는 늘 논쟁거리죠
20:13:56 &lt;zzz&gt; 홍보팀이 더 알릴 수 있을 겁니다, 분명히요
20:14:10 &lt;orignal&gt; 저는 항상 릴리스 일주일 전에 하도록 하겠습니다
20:14:16 &lt;i2pr&gt; [Slack/str4d] zzz, IRC 알림용 설정을 i2p.i2p에 방금 푸시했습니다
20:14:34 &lt;zzz&gt; 추가로, 일정 관련 메모입니다. 다음 회의들은 CCC에서 대면으로 진행됩니다. 1월 2일에는 회의를 하지 않습니다.
20:14:35 &lt;orignal&gt; 적어도 주제가 생기겠죠
20:14:44 &lt;zzz&gt; 다음 IRC 회의는 2월 6일(화)입니다
20:15:33 &lt;zzz&gt; CCC 회의 주제는 zzz.i2p의 스레드를 확인해 주세요
20:15:42 &lt;zzz&gt; 의견이 있으면 거기에 추가해 주세요
20:15:47 &lt;zzz&gt; 회의에 대해 다른 내용 있나요?
20:15:52 * zzz baffer를 잡는다
20:16:58 &lt;i2pr&gt; [Slack/str4d] CCC 전에 제안서 작업을 더 진행하겠습니다
20:17:11 * zzz *bafs* 회의 종료 </div>
