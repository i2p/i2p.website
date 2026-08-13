---
title: "I2PControl JSON-RPC"
description: "I2PControl 웹앱을 통한 원격 router 관리 API"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# I2PControl API 문서

-------------확인 추가 사항--------------

I2PControl은 I2P router와 함께 번들로 제공되는 **JSON-RPC 2.0** API입니다 (버전 0.9.39부터). 구조화된 JSON 요청을 통해 router의 인증된 모니터링 및 제어를 가능하게 합니다.

> **기본 비밀번호:** `itoopie` — 이는 공장 기본값이며 보안을 위해 **즉시 변경해야 합니다**.

## 1. 개요 및 접근

| 구현체                     | 기본 엔드포인트                          | 프로토콜  | 기본 활성화 여부                             | 비고                   |
|----------------------------|----------------------------------------|---------|---------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/`       | HTTP    | ❌ 웹앱(Router Console)에서 수동 활성화 필요   | 번들된 웹앱            |
| i2pd (C++ 구현체)          | `https://127.0.0.1:7650/`              | HTTPS   | ✅ 기본적으로 활성화됨                         | 레거시 플러그인 동작     |
---

Java I2P의 경우, **Router Console → WebApps → I2PControl**로 이동하여 활성화해야 합니다(자동으로 시작하도록 설정). 활성화되면 모든 메서드는 먼저 인증하고 세션 토큰을 받아야 합니다.

## 2. JSON-RPC 형식

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
모든 요청은 JSON-RPC 2.0 구조를 따릅니다:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
성공적인 응답에는 `result` 필드가 포함되고, 실패 시에는 `error` 객체가 반환됩니다:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
또는

## 3. 인증 플로우

### 요청 (인증)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### 성공적인 응답

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| 필드       | 방향      | 유형   | 설명                                                     |
|------------|-----------|--------|----------------------------------------------------------|
| `API`      | 요청      | long   | 클라이언트가 요청하는 I2PControl API 버전. `1`을 사용하세요. |
| `Password` | 요청      | String | I2PControl에 인증하기 위해 사용하는 비밀번호.             |
| `API`      | 응답      | long   | 서버에서 구현한 주요 API 버전.                           |
| `Token`    | 응답      | String | 후속 요청에 사용되는 인증 토큰.                          |
---

이후의 모든 요청에서 해당 `Token`을 `params`에 포함해야 합니다.

## 4. 메소드 및 엔드포인트

### 4.1 RouterInfo

---

router에 대한 주요 원격 측정 데이터를 가져옵니다.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**요청 예제**

#### 상태 코드 열거형 (`i2p.router.net.status`)

| Key                                    | Type   | Description                                                             |
|----------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                    | String | 표시를 위한 자유 형식의 번역된 라우터 상태입니다.                      |
| `i2p.router.uptime`                    | long   | 라우터 가동 시간(밀리초 단위). 오래된 i2pd 버전은 문자열을 반환할 수 있습니다. |
| `i2p.router.version`                   | String | 전체 라우터 버전.                                                       |
| `i2p.router.net.status`                | long   | 네트워크 상태 코드; 아래 표를 참조하세요.                               |
| `i2p.router.net.bw.inbound.1s`         | double | 현재 수신 대역폭(초당 바이트).                                          |
| `i2p.router.net.bw.inbound.15s`        | double | 15초 평균 수신 대역폭(초당 바이트).                                     |
| `i2p.router.net.bw.outbound.1s`        | double | 현재 송신 대역폭(초당 바이트).                                          |
| `i2p.router.net.bw.outbound.15s`       | double | 15초 평균 송신 대역폭(초당 바이트).                                     |
| `i2p.router.net.tunnels.participating` | long   | 이 라우터가 참여 중인 터널의 수.                                        |
#### 상태 코드 열거형(`i2p.router.net.status`)

| 코드 | 의미                                                  |
|------|-------------------------------------------------------|
| 0    | 정상                                                  |
| 1    | 테스트 중                                             |
| 2    | 방화벽 차단됨                                         |
| 3    | 숨겨짐                                               |
| 4    | 경고: 방화벽 차단 및 속도 빠름                         |
| 5    | 경고: 방화벽 차단 및 플러드필 노드                    |
| 6    | 경고: 방화벽 차단 및 TCP 수신 연결 존재               |
| 7    | 경고: 방화벽 차단 및 UDP 비활성화됨                   |
| 8    | 오류 I2CP                                             |
| 9    | 오류: 시계 오차(시간 불일치)                          |
| 10   | 오류: 개인 TCP 주소                                 |
| 11   | 오류: 대칭형 NAT                                      |
| 12   | 오류: UDP 포트 사용 중                                |
| 13   | 오류: 활성 피어 없음. 연결 및 방화벽 확인 필요        |
| 14   | 오류: UDP 비활성화 및 TCP 설정되지 않음               |
#### NetDB 및 피어 필드

| Key                                  | Type    | Description                                        |
|--------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | 로컬 라우터를 제외한 알려진 피어의 수입니다.       |
| `i2p.router.netdb.activepeers`       | long    | 활성 상태인 피어의 수입니다.                       |
| `i2p.router.netdb.fastpeers`         | long    | 빠른(fast)으로 분류된 피어의 수입니다.             |
| `i2p.router.netdb.highcapacitypeers` | long    | 고용량(high capacity)으로 분류된 피어의 수입니다.  |
| `i2p.router.netdb.isreseeding`       | boolean | 재시딩(reseed)이 진행 중인지 여부입니다.          |
**응답 필드 (result)**   공식 문서(GetI2P)에 따르면:   - `i2p.router.status` (String) — 사람이 읽을 수 있는 상태   - `i2p.router.uptime` (long) — 밀리초 (또는 이전 i2pd의 경우 문자열) :contentReference[oaicite:0]{index=0}   - `i2p.router.version` (String) — 버전 문자열 :contentReference[oaicite:1]{index=1}   - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — B/s 단위의 인바운드 대역폭 :contentReference[oaicite:2]{index=2}   - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — B/s 단위의 아웃바운드 대역폭 :contentReference[oaicite:3]{index=3}   - `i2p.router.net.status` (long) — 숫자 상태 코드 (아래 enum 참조) :contentReference[oaicite:4]{index=4}   - `i2p.router.net.tunnels.participating` (long) — 참여 중인 tunnel 수 :contentReference[oaicite:5]{index=5}   - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — netDB 피어 통계 :contentReference[oaicite:6]{index=6}   - `i2p.router.netdb.isreseeding` (boolean) — reseed가 활성화되어 있는지 여부 :contentReference[oaicite:7]{index=7}   - `i2p.router.netdb.knownpeers` (long) — 알려진 총 피어 수 :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| 매개변수 | 유형 | 설명 |
|-----------|--------|------------------------------|
| `Stat`    | 문자열 | 라우터 RateStat 이름.        |
| `Period`  | long   | 밀리초 단위의 비율 주기. |
주어진 시간 창에서 속도 메트릭(예: 대역폭, tunnel 성공률)을 가져오는 데 사용됩니다.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**요청 예제**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**샘플 응답**

### 4.3 RouterManager

---

| 매개변수            | 결과            | 설명                                                           |
|--------------------|-------------------|-----------------------------------------------------------------------|
| `Restart`          | null              | 즉시 라우터를 재시작합니다.                                |
| `RestartGraceful`  | null              | 참여 중인 터널이 만료된 후 재시작합니다.                          |
| `Shutdown`         | null              | 즉시 라우터를 종료합니다.                               |
| `ShutdownGraceful` | null              | 참여 중인 터널이 만료된 후 종료합니다.                        |
| `Reseed`           | null              | 라우터 리시드를 시작합니다.                                               |
| `FindUpdates`      | boolean 또는 String | 블로킹. 서명된 라우터 업데이트를 검색합니다.                        |
| `Update`           | String            | 블로킹. 서명된 라우터 업데이트를 시작하고 최종 상태를 반환합니다. |
관리 작업을 수행합니다.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**허용되는 매개변수 / 메소드**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**요청 예시**

### 4.4 NetworkSetting

**성공적인 응답**

---

| 키                                  | 허용되는 값                                       | 설명                                                         |
|------------------------------------|--------------------------------------------------|--------------------------------------------------------------|
| `i2p.router.net.ntcp.port`         | 문자열, 1–65535                                   | NTCP 포트; 변경 시 재시작 필요.                              |
| `i2p.router.net.ntcp.hostname`     | 문자열                                           | NTCP 호스트명; 변경 시 재시작 필요.                           |
| `i2p.router.net.ntcp.autoip`       | `always`, `true`, 또는 `false`                   | NTCP 자동 주소 선택.                                         |
| `i2p.router.net.ssu.port`          | 문자열, 1–65535                                   | SSU 포트; 변경 시 재시작 필요.                                |
| `i2p.router.net.ssu.hostname`      | 문자열                                           | SSU 외부 호스트명; 변경 시 재시작 필요.                       |
| `i2p.router.net.ssu.autoip`          | `ssu`, `local,ssu`, `upnp,ssu`, 또는 `local,upnp,ssu` | SSU 주소 탐지 소스.                                          |
| `i2p.router.net.ssu.detectedip`    | null                                             | 읽기 전용으로 감지된 SSU 주소.                               |
| `i2p.router.net.upnp`              | 문자열                                           | UPnP 설정.                                                   |
| `i2p.router.net.bw.share`          | 문자열, 0–100                                     | 참가 터널에 사용 가능한 대역폭의 백분율.                    |
| `i2p.router.net.bw.in`             | 음이 아닌 정수 문자열                            | 수신 대역폭 제한(KiB/s 단위).                                |
| `i2p.router.net.bw.out`            | 음이 아닌 정수 문자열                            | 송신 대역폭 제한(KiB/s 단위).                                |
| `i2p.router.net.laptopmode`        | 문자열                                           | 노트북 모드 설정.                                            |
네트워크 구성 매개변수(포트, upnp, 대역폭 공유 등)를 가져오거나 설정합니다

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**요청 예시 (현재 값 가져오기)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**샘플 응답**

> 참고: 2.41 이전 버전의 i2pd는 문자열 대신 숫자 타입을 반환할 수 있습니다 — 클라이언트는 두 가지 모두를 처리해야 합니다. :contentReference[oaicite:11]{index=11}

### 4.5 고급 설정

---

| 매개변수 | 형식                  | 설명                                                                  |
|---------|-----------------------|----------------------------------------------------------------------|
| `get`   | 문자열                | `get` 결과 객체 내에서 하나의 설정 값을 반환합니다.                     |
| `getAll`| 없음                  | `getAll` 내에서 전체 구성 맵을 반환합니다.                              |
| `set`   | Map<String, String>  | 다른 키를 제거하지 않고 제공된 설정들을 업데이트합니다.                   |
| `setAll`| Map<String, String>  | **파괴적 동작:** 제공되지 않은 키들을 모두 제거하며 모든 설정을 대체합니다. |
내부 router 매개변수를 조작할 수 있게 합니다.

**요청 예시**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**응답 예제**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### 표준 JSON-RPC2 오류 코드

---

| 매개변수 | 형식 | 설명 |
|-----------|--------|-----------------------------|
| `Echo`    | 문자열 | `Result`로 반환되는 값. |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### I2PControl 특정 오류 코드

I2PControl 자체를 관리합니다. 현재의 자바 핸들러는 비밀번호 변경을 지원합니다.

| 매개변수               | 유형   | 설명                                                                       |
|-----------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password` | 문자열 | 새로운 I2PControl 비밀번호를 설정하고 기존 인증 토큰을 폐기합니다.            |
결과에 `SettingsSaved`가 포함됩니다. 비밀번호가 변경된 경우, 결과에는 `"i2pcontrol.password": null`도 함께 포함됩니다. 기존의 독립 실행형 플러그인에서 사용하던 listen-address 및 listen-port 설정은 현재의 Java 핸들러에서는 비활성화되어 있습니다.

> **기본 비밀번호:** `itoopie` — 이는 공장 기본값이며 보안을 위해 **즉시 변경해야 합니다**.

## 5. 오류 코드

### 표준 JSON-RPC2 오류 코드

| 코드   | 의미               |
|--------|--------------------|
| -32700 | JSON 파싱 오류     |
| -32600 | 잘못된 요청        |
| -32601 | 메서드를 찾을 수 없음 |
| -32602 | 잘못된 매개변수    |
| -32603 | 내부 오류          |
### I2PControl 전용 오류 코드

| 코드   | 의미                                                                                  |
|--------|------------------------------------------------------------------------------------------|
| -32001 | 잘못된 비밀번호 제공됨                                                                |
| -32002 | 인증 토큰이 제출되지 않음                                                             |
| -32003 | 제출된 인증 토큰이 존재하지 않음                                                       |
| -32004 | 제공된 인증 토큰이 만료되어 삭제될 것임                                                |
| -32005 | 사용된 I2PControl API 버전이 지정되지 않았지만, 지정해야 함                            |
| -32006 | 지정된 I2PControl API 버전이 I2PControl에서 지원되지 않음                              |
> **기본 비밀번호:** `itoopie` — 이는 공장 기본값이며 보안을 위해 **즉시 변경해야 합니다**.

## 6. 사용법 및 모범 사례

- 인증 시를 제외하고 항상 `Token` 매개변수를 포함하세요.
- 첫 사용 시 기본 비밀번호(`itoopie`)를 변경하세요.
- Java I2P의 경우, WebApps를 통해 I2PControl webapp이 활성화되어 있는지 확인하세요.
- 약간의 차이에 대비하세요: I2P 버전에 따라 일부 필드가 숫자 또는 문자열일 수 있습니다.
- 표시 친화적 출력을 위해 긴 상태 문자열을 줄바꿈하세요.

> **기본 비밀번호:** `itoopie` — 이는 공장 기본값이며 보안을 위해 **즉시 변경해야 합니다**.
