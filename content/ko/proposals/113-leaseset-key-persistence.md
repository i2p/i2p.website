---
title: "LeaseSet 키 지속성"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Closed"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## 개요

이 제안은 현재 일시적인 LeaseSet에 추가 데이터를 지속시키는 것에 관한 것입니다.
0.9.18에 구현되었습니다.

## 동기

0.9.17에서는 i2ptunnel.config에 저장된 netDb 슬라이싱 키에 대한 지속성이 추가되었습니다. 이는 재시작 후 동일한 슬라이스를 유지하여 몇 가지 공격을 방지하는 데 도움이 되며, 라우터 재시작과의 가능한 상관관계도 방지합니다.

라우터 재시작과 더 쉽게 상관관계를 가질 수 있는 다른 두 가지는 leaseset 암호화 및 서명 키입니다. 현재 이들은 지속화되지 않습니다.

## 제안된 변경 사항

개인 키는 i2ptunnel.config에 i2cp.leaseSetPrivateKey 및 i2cp.leaseSetSigningPrivateKey로 저장됩니다.
