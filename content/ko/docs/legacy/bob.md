---
title: "BOB – Basic Open Bridge(기본 오픈 브리지)"
description: "목적지 관리용 사용 중단된 API(사용 중단됨)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **경고:** BOB은 레거시 DSA-SHA1 서명 유형만 지원합니다. Java I2P는 **1.7.0 (2022-02)**부터 BOB을 더 이상 제공하지 않으며; 1.6.1 또는 그 이전 버전으로 설치를 시작한 환경과 일부 i2pd 빌드에만 남아 있습니다. 새로운 애플리케이션은 **반드시** [SAM v3](/docs/api/samv3/)를 사용해야 합니다.

## 언어 바인딩

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## 프로토콜 참고 사항

- `KEYS`는 base64 목적지(공개 + 개인 키)를 나타냅니다.  
- `KEY`는 base64 공개 키입니다.  
- `ERROR` 응답은 `ERROR <description>\n` 형식을 갖습니다.  
- `OK`는 명령 완료를 나타내며; 선택적 데이터가 같은 줄에 이어집니다.  
- `DATA` 줄은 최종 `OK` 전에 추가 출력을 스트리밍합니다.

`help` 명령만이 유일한 예외입니다: “해당 명령이 없습니다”를 나타내기 위해 아무것도 반환하지 않을 수 있습니다.

## 연결 배너

BOB는 개행(LF 또는 CRLF)으로 끝나는 ASCII 줄을 사용합니다. 연결되면 다음을 출력합니다:

```
BOB <version>
OK
```
현재 버전: `00.00.10`. 이전 빌드는 대문자 16진수와 비표준 버전 번호 체계를 사용했습니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## 핵심 명령어

> 모든 명령어에 대한 자세한 정보는 `telnet localhost 2827`로 연결한 뒤 `help`를 실행하세요.

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## 사용 중단 요약

- BOB(I2P의 구형 브리지 프로토콜)은 최신 서명 유형, 암호화된 LeaseSets, 또는 전송 계층 기능을 지원하지 않습니다.
- API는 동결되어 있어 새로운 명령이 추가되지 않습니다.
- 여전히 BOB에 의존하는 애플리케이션은 가능한 한 빨리 SAM v3로 마이그레이션해야 합니다.
