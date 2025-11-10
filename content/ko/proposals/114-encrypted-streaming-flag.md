---
title: "'Encrypted' Streaming Flag"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/1795"
---

## 개요

이 제안서는 스트리밍에 사용되고 있는 종단간 암호화 유형을 지정하는 플래그를 추가하는 것에 관한 것입니다.

## 동기

높은 부하를 받는 앱들은 ElGamal/AES+SessionTags 태그의 부족을 겪을 수 있습니다.

## 설계

스트리밍 프로토콜 내 어딘가에 새 플래그를 추가합니다. 이 플래그가 포함된 패킷이 오면, 페이로드는 개인 키와 피어의 공개 키로부터 얻은 키로 AES 암호화되어 있다는 것을 의미합니다. 이는 마늘 (ElGamal/AES) 암호화를 제거하고 태그 부족 문제를 해결할 수 있게 합니다.

패킷당 또는 스트림당으로 SYN을 통해 설정할 수 있습니다.
