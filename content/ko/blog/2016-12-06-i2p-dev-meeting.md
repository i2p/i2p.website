---
title: "I2P 개발자 회의 - 2016년 12월 6일"
date: 2016-12-06
author: "zzz"
description: "2016년 12월 6일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> echelon, manas, orignal, zzz</p>

## 회의 기록

<div class="irc-log">20:00:02 &lt;zzz&gt; 0) 안녕하세요
20:00:02 &lt;zzz&gt; 1) 33C3 계획
20:00:02 &lt;zzz&gt; 2) 0.9.28 업데이트 (zzz)
20:00:02 &lt;zzz&gt; 3) Tails 메인테이너 (zzz) http://zzz.i2p/topics/2108
20:00:07 &lt;zzz&gt; 0) 안녕하세요
20:00:09 &lt;zzz&gt; 안녕
20:00:16 &lt;i2pr&gt; [Slack/manas] 안녕하세요 :slightly_smiling_face:
20:00:44 &lt;zzz&gt; 1) 33C3 계획
20:00:54 &lt;orignal_&gt; 안녕
20:01:08 &lt;zzz&gt; 좋아요, 오늘로부터 3주인데, 논의해야 할 게 있나요?
20:01:38 &lt;eche|on&gt; 적어도 트위터로는 연락 가능합니다
20:01:49 &lt;eche|on&gt; 12월 26일부터 함부르크에 있습니다 
20:01:53 &lt;zzz&gt; 트위터 DM 그룹은 이틀 정도 전에 만들어둘 거라고 봅니다
20:01:58 &lt;eche|on&gt; 배너랑 노트북, 스티커를 가져갈게요
20:02:10 &lt;i2pr&gt; [Slack/manas] 12월 26일 오후에 함부르크에 도착할 예정입니다
20:02:11 &lt;zzz&gt; 저도 스티커 가져갈게요.
20:02:21 &lt;zzz&gt; 멀티탭 잊지 마세요
20:02:39 &lt;eche|on&gt; 티켓들은 전부 결제했고, 사람들에게 나눠드리는 건 제가 관리할게요
20:02:45 &lt;zzz&gt; 늘 하던 대로, 26일에 도착한 사람들이 테이블을 잡습니다
20:02:45 &lt;eche|on&gt; ok
20:02:57 &lt;i2pr&gt; [Slack/manas] 처음 CCC 가는 사람들을 위한 팁/조언이 있을까요?
20:02:57 &lt;eche|on&gt; 네
20:03:12 &lt;zzz&gt; Monero 쪽은 fluffypony 포함 2명
20:03:29 &lt;eche|on&gt; manas: 와서 전부 흡수하고, 시스템이 24/7 두들겨 맞을 준비를 하세요, 큰 하드디스크 준비하고, 약간의 돈도 준비하고, 예상치 못한 일을 예상하세요^^
20:03:30 &lt;zzz&gt; 일반적인 팁은 회의 끝나고 알려줄게요
20:03:35 &lt;i2pr&gt; [Slack/manas] :smile:
20:03:41 &lt;zzz&gt; 1) 관련해서 더 있나요?
20:04:48 &lt;zzz&gt; 2) 0.9.28 업데이트
20:04:55 &lt;eche|on&gt; 그냥: 33C3가 잘 되길 바랍니다
20:05:19 &lt;zzz&gt; 0.9.28은 일정대로 진행 중이고, 체크인과 번역 마감은 금요일입니다. 다음 주 초에 릴리즈할 수 있을 겁니다
20:05:35 &lt;zzz&gt; 이번 주말에 diff 검토 좀 도와주세요
20:05:57 &lt;orignal_&gt; 제가 알아둬야 할 새로운 게 있나요?
20:06:09 &lt;orignal_&gt; 그러니까 0.9.28 말이에요
20:06:09 &lt;eche|on&gt; 좋아요, 12월 19일까지 여기서 이것저것 할 거고, 20일부터는 하루에 몇 시간 정도 온라인입니다
20:06:22 &lt;zzz&gt; 그런 건 없는 것 같아요, orignal_ 
20:06:28 &lt;zzz&gt; 2) 관련해서 더 있나요?
20:06:53 &lt;orignal_&gt; 감사합니다
20:07:34 &lt;zzz&gt; 3) Tails 메인테이너
20:07:49 &lt;zzz&gt; Tails 쪽 상황이 안 좋습니다. 올해 메인테이너 3명이 사라졌습니다
20:08:23 &lt;zzz&gt; Tails 개발자 중 일부는, 수년간 티켓에 신경을 쓰지 않은 것과 안정적인 유지보수의 부재 때문에, Tails에서 i2p를 제거하길 원합니다
20:08:47 &lt;zzz&gt; 오늘 아침 sadie가 트윗을 올렸고, 한 명이 응답했습니다
20:09:26 &lt;zzz&gt; sadie가 크게 PR을 밀어야 할지도... 아니면 이번 새로운 자원봉사자가 잘 해줄지도 모르겠네요
20:09:36 &lt;zzz&gt; 자원해 줄 분 있나요, 아이디어 있는 분?
20:10:34 &lt;zzz&gt; 좋아요, 트위터로 온 자원봉사자에게 답하고 진행 상황을 보겠습니다
20:10:41 &lt;zzz&gt; 3) 관련해서 더 있나요?
20:11:34 &lt;zzz&gt; 회의에서 더 논의할 것 있나요?
20:11:35 &lt;i2pr&gt; [Slack/manas] 도와드리고 싶지만 이 부분은 익숙하지 않아서, 많은 자료를 읽고 배워야 할 것 같습니다.
20:11:46 &lt;i2pr&gt; [Slack/manas] 관련 스레드를 열어놨습니다, 읽어보겠습니다
20:12:01 &lt;zzz&gt; i2p, Tails, 그리고 Debian 패키지 경험이 필요합니다
20:12:08 &lt;i2pr&gt; [Slack/manas] 제 reseed(부트스트랩 노드)의 SSL 인증서가 만료되었거나 곧 만료될 수 있어서, 업데이트해 두겠습니다
20:12:19 &lt;orignal_&gt; I2P는 지금보다 PR을 더 해야 합니다
20:12:54 &lt;zzz&gt; orignal_, 동의합니다. 아이디어가 있으면 sadie와 str4d에게 전달해 주세요
20:12:56 &lt;i2pr&gt; [Slack/manas] letskencrypt(현재 이름은 acme-client)이 여러 번 바뀌었지만 이제 안정되었습니다. reseed들의 SSL 인증서 업데이트를 자동화할 수 있습니다.
20:13:09 &lt;i2pr&gt; [Slack/manas] 그래서 reseed들이 일시적으로 내려갈 수 있지만 곧 돌아올 겁니다 :slightly_smiling_face:
20:13:18 &lt;zzz&gt; manas, reseed 관련 문제는 backup@mail.i2p와 함께 진행하세요
20:13:24 &lt;zzz&gt; 회의에서 더 논의할 것 있나요?
20:13:28 &lt;i2pr&gt; [Slack/manas] 네
20:14:44 &lt;zzz&gt; 1월 첫째 주에는 회의가 없습니다. CCC에서 대면 회의를 진행할 예정입니다. 자세한 내용은 이 채널을 확인하세요, 회의가 짧은 공지로 잡힐 수도 있습니다
20:15:10 &lt;zzz&gt; 가능한 회의 목록은 zzz.i2p의 스레드에 있습니다. 주제를 추가하거나 원격 참여를 요청하려면 그곳에서 말씀해 주세요
20:15:23 * zzz **bafs** 회의를 종료합니다 </div>
