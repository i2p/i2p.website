---
title: "멀티캐스트"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Dead"
thread: "http://zzz.i2p/topics/172"
---

## 개요

기본 아이디어: 아웃바운드 터널을 통해 한 번의 복사본을 보내고, 아웃바운드 엔드포인트가 모든 인바운드 게이트웨이에 분배합니다. 단말 간 암호화는 제외됩니다.


## 설계

- 새로운 멀티캐스트 터널 메시지 타입 (전달 타입 = 0x03)
- 아웃바운드 엔드포인트 멀티캐스트 분배
- 새로운 I2NP 멀티캐스트 메시지 타입?
- 새로운 I2CP 멀티캐스트 SendMessageMessage 메세지 타입
- OutNetMessageOneShotJob에서 라우터 간 암호화 하지 않기 (garlic?)

앱:

- RTSP 프록시?

스트리머:

- MTU 조정? 아니면 그냥 앱에서 처리?
- 요청 시 수신 및 전송
