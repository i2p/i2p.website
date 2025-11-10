---
title: "I2P 개발자 회의, 2003년 9월 2일"
date: 2003-09-02
author: "jrand0m"
description: "사양 및 SDK 릴리스, 개발 현황, 향후 프로젝트를 다루는 제56회 I2P 개발자 회의"
categories: ["meeting"]
---

<h2 id="quick-recap">Quick recap</h2>

<p class="attendees-inline"><strong>참석자:</strong> jrand0m, mihi, shardy, thecrypto, w0rmus</p>

<h2 id="meeting-log">회의 기록</h2>

<div class="irc-log"> [22:53] <jrand0m> 좋아, 뭐 어때, 해보지 뭐.  안건: [22:53] <jrand0m> 0) 환영 [22:53] <jrand0m> 1) 스펙 &amp; sdk 릴리스 [22:53] <jrand0m> 2) 스펙 &amp; sdk 질문 [22:53] <jrand0m> 3) 개발 현황 3.1) co's NS 3.2) sdk 1.0 기준 3.3) 네트워크 시뮬레이터 3.4) 기타 앱 [IM, tunnel, 등] 3.5) 더 많은 트랜스포트 3.6) java router 구현 [22:53] <jrand0m> 4) 회의 시간 변경? [22:53] <jrand0m> 5) cvs 행정 잡무 [22:54] <jrand0m> 6) shardy의 것들 [22:54] <jrand0m> 7) 방청석 [22:54] <jrand0m> 그게 다임. [22:54] <jrand0m> 0) 환영 [22:54] <w0rmus> 하이하이 [22:54] <thecrypto> 자, 모두 제55차 회의에 오신 것을 환영합니다 [22:54] <thecrypto> 56 [22:55] <thecrypto> 56이 맞습니다 [22:55] *** 퇴장: mihi (클라이언트로부터 EOF) [22:55] <jrand0m> 안녕.  제56차 회의에 오신 것을 환영합니다 [22:55] <jrand0m> 그래 [22:55] <jrand0m> 1) 스펙 &amp; sdk 릴리스 [22:55] <w0rmus> 하하 [22:55] *** mihi (~none@anon.iip)님이 채널 #iip-dev에 참가했습니다 [22:55] <jrand0m> 스펙이 공개됐고 sdk 0.2도 나왔습니다. [22:56] <jrand0m> 현재는 freenet에서만 이용 가능합니다 [http://localhost:8888/CHK@p1VU1U67UgXYJ7v7cS4Xqn~p4ssLAwI,RvdwV4jZyZYcJgYabpVPOQ/I2P_SDK.zip] [22:56] <jrand0m> 하지만 nop이 오늘 일반 웹에도 올리고, 기존 리스트 몇 곳에 이메일을 보내서 리뷰어들을 모으겠다고 했습니다 [22:57] <jrand0m> 2) 스펙이나 sdk에 대한 새로운 질문 있나요? [22:58] *** nixonite (~nixonite@anon.iip)님이 채널 #iip-dev에 참가했습니다 [22:58] *** terrific (terrific@anon.iip)님이 채널 #iip-dev에 참가했습니다 [22:58] <jrand0m> 음, 첫 번째 질문은, 스펙을 /읽는/ 진행 상황이 어떤가요?  :) [22:58] <w0rmus> 그거 해야지 :) [22:58] <thecrypto> 천천히

[회의 기록은 명세, SDK 개발, 네트워크 시뮬레이터, 기타 프로젝트에 대한 논의로 이어집니다. 회의에서는 개발 현황 업데이트와 향후 릴리스 계획을 다룹니다.] </div>
