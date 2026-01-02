---
title: "I2P Router 문제 해결 가이드"
description: "연결성, 성능 및 구성 문제를 포함한 일반적인 I2P router 문제에 대한 종합적인 문제 해결 가이드"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

I2P router가 실패하는 가장 흔한 원인은 **포트 포워딩 문제**, **불충분한 대역폭 할당**, **부적절한 부트스트랩(초기 네트워크 동기화) 시간**입니다. 이 세 가지 요인이 보고된 문제의 70% 이상을 차지합니다. router는 시작 후 네트워크에 완전히 통합되려면 최소 **10-15분**이 필요하며, **128 KB/sec 최소 대역폭**(256 KB/sec 권장)과 적절한 **UDP/TCP 포트 포워딩**이 있어야 방화벽에 막히지 않은 상태를 달성할 수 있습니다. 새 사용자는 즉각적인 연결을 기대하고 너무 일찍 재시작하는 경우가 흔한데, 이로 인해 통합 진행 상황이 초기화되어 좌절스러운 악순환이 생깁니다. 이 가이드는 2.10.0 이상 버전에 영향을 미치는 주요 I2P 문제 전반에 대한 자세한 해결책을 제공합니다.

I2P의 익명성 아키텍처는 암호화된 다중 홉 tunnel을 사용하기 때문에 본질적으로 프라이버시를 위해 속도를 대가로 치릅니다. 이러한 근본적인 설계를 이해하면 사용자는 정상적인 동작을 문제로 오해하지 않고 현실적인 기대치를 설정하고 효과적으로 문제를 해결할 수 있습니다.

## Router가 시작되지 않거나 즉시 충돌합니다

가장 흔한 시작 실패는 **포트 충돌**, **Java 버전 비호환성**, 또는 **손상된 구성 파일**에서 비롯됩니다. 더 깊은 문제를 조사하기 전에 다른 I2P 인스턴스가 이미 실행 중인지 확인하세요.

**충돌하는 프로세스가 없는지 확인:**

리눅스: `ps aux | grep i2p` 또는 `netstat -tulpn | grep 7657`

Windows: 작업 관리자 → 세부 정보 → 명령줄에 i2p가 포함된 java.exe를 찾으세요

macOS: 활동 모니터 → "i2p" 검색

좀비 프로세스가 있다면 강제 종료하세요: `pkill -9 -f i2p` (Linux/Mac) 또는 `taskkill /F /IM javaw.exe` (Windows)

**Java 버전 호환성 확인:**

I2P 2.10.0+는 **최소 Java 8**이 필요하며, Java 11 이상을 권장합니다. 설치가 "mixed mode"("interpreted mode"가 아님)로 표시되는지 확인하세요:

```bash
java -version
```
다음이 표시되어야 합니다: OpenJDK 또는 Oracle Java, 버전 8+, "mixed mode"

**피하십시오:** GNU GCJ, 구식 Java 구현체, 인터프리터 전용 모드

**일반적인 포트 충돌**은 여러 서비스가 I2P의 기본 포트를 두고 경쟁할 때 발생합니다. router console (7657), I2CP (7654), SAM (7656), 그리고 HTTP 프록시 (4444)는 사용 가능해야 합니다. 충돌 여부 확인: `netstat -ano | findstr "7657 4444 7654"` (Windows) 또는 `lsof -i :7657,4444,7654` (Linux/Mac).

**구성 파일 손상**은 로그에 구문 분석 오류가 기록되며 즉시 충돌이 발생하는 형태로 나타납니다. Router.config는 **BOM 없는 UTF-8 인코딩**을 요구하고, 구분자로 `=`를 사용합니다 ( `:` 아님), 또한 특정 특수 문자는 금지됩니다. 백업한 뒤 다음을 확인하세요: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

식별 정보를 유지하면서 구성을 초기화하려면: I2P를 중지하고, router.keys와 keyData 디렉터리를 백업한 뒤, router.config를 삭제하고 재시작하십시오. router가 기본 구성을 다시 생성합니다.

**Java 힙 할당량이 너무 낮으면** OutOfMemoryError(메모리 부족 오류) 충돌이 발생합니다. wrapper.config를 편집하고 `wrapper.java.maxmemory`를 기본값 128 또는 256에서 **최소 512**(고대역폭 routers의 경우 1024)로 늘리세요. 이 변경을 적용하려면 완전히 종료하고 11분을 기다렸다가 다시 시작해야 합니다 - 콘솔에서 "Restart"를 클릭해도 변경 사항은 적용되지 않습니다.

## "Network: Firewalled" 상태 해결

방화벽 상태란 router가 직접적인 인바운드 연결을 수신할 수 없어 introducers(소개자 노드)에 의존해야 함을 의미합니다. router는 이 상태에서도 동작하지만, **성능이 크게 저하됩니다** 그리고 네트워크에 대한 기여도는 최소 수준에 머뭅니다. 방화벽에 의해 차단되지 않은 상태를 달성하려면 올바른 포트 포워딩이 필요합니다.

**router는 포트를 무작위로 선택합니다**(통신용 범위: 9000-31000). http://127.0.0.1:7657/confignet 에서 자신의 포트를 확인하세요 - "UDP Port"와 "TCP Port"를 찾으면 됩니다(일반적으로 같은 번호입니다). 최적의 성능을 위해서는 **UDP와 TCP 둘 다** 포트 포워딩을 해야 하지만, UDP만으로도 기본 기능은 동작합니다.

**UPnP 자동 포트 포워딩 활성화** (가장 간단한 방법):

1. http://127.0.0.1:7657/confignet에 접속하세요
2. "Enable UPnP"를 선택하세요
3. 변경 사항을 저장하고 router를 다시 시작하세요
4. 5~10분 기다린 후 상태가 "Network: Firewalled"에서 "Network: OK"로 변경되었는지 확인하세요

UPnP는 router 지원(2010년 이후 제조된 대부분의 소비자용 router에서는 기본적으로 활성화됨)과 적절한 네트워크 구성을 필요로 합니다.

**수동 포트 포워딩** (UPnP가 실패할 때 필요):

1. http://127.0.0.1:7657/confignet 에서 자신의 I2P 포트를 확인해 메모해 두세요 (예: 22648)
2. 로컬 IP 주소를 확인하세요: `ipconfig` (Windows), `ip addr` (Linux), 시스템 환경설정 → 네트워크 (macOS)
3. router의 관리자 인터페이스에 접속하세요 (일반적으로 192.168.1.1 또는 192.168.0.1)
4. Port Forwarding으로 이동하세요 (Advanced, NAT, 또는 Virtual Servers 아래에 있을 수 있음)
5. 다음 두 가지 규칙을 생성하세요:
   - 외부 포트: [당신의 I2P 포트] → 내부 IP: [당신의 컴퓨터] → 내부 포트: [동일] → 프로토콜: **UDP**
   - 외부 포트: [당신의 I2P 포트] → 내부 IP: [당신의 컴퓨터] → 내부 포트: [동일] → 프로토콜: **TCP**
6. 구성을 저장하고 필요한 경우 router를 재시작하세요

**포트 포워딩 검증**은 설정을 마친 뒤 온라인 점검 도구로 수행하세요. 감지되지 않으면 방화벽 설정을 확인하세요 - 시스템 방화벽과 백신 방화벽 모두에서 I2P 포트를 허용해야 합니다.

**Hidden mode 대안** 포트 포워딩이 불가능한 제한적인 네트워크 환경에서 사용: http://127.0.0.1:7657/confignet에서 활성화 → "Hidden mode"를 체크하세요. router는 방화벽 뒤 상태를 유지하지만, SSU introducers(SSU에서 NAT 우회를 위한 소개자)를 전용으로 사용해 이 상태에 최적화합니다. 성능은 느려지지만 정상적으로 동작합니다.

## router가 "Starting" 또는 "Testing" 상태에서 멈춰 있음

초기 부트스트랩 과정에서 나타나는 이러한 일시적 상태들은 **신규 설치의 경우 10-15분** 또는 **기존 routers의 경우 3-5분** 내에 대개 해소됩니다. 너무 일찍 개입하면 오히려 문제를 악화시키는 경우가 많습니다.

**"Network: Testing"**는 router가 다양한 연결 방식(직접, introducers(소개자 노드), 여러 프로토콜 버전)을 통해 도달 가능성을 점검하고 있음을 의미합니다. 이는 시작 후 처음 5-10분 동안 정상입니다. router는 최적 구성을 결정하기 위해 여러 시나리오를 테스트합니다.

**"Rejecting tunnels: starting up"**은 router에 충분한 피어 정보가 없을 때 bootstrap(초기 설정) 중에 나타납니다. router는 네트워크에 충분히 통합될 때까지 중계 트래픽에 참여하지 않습니다. netDb에 50개 이상의 router가 채워지면 보통 10~20분 후 이 메시지는 사라집니다.

**클록 스큐는 도달성 테스트를 무력화합니다.** I2P는 시스템 시간이 네트워크 시간과 **±60초** 이내여야 합니다. 90초를 초과하는 차이가 있으면 연결이 자동으로 거부됩니다. 시스템 시계를 동기화하십시오:

리눅스: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: 제어판 → 날짜 및 시간 → 인터넷 시간 → 지금 업데이트 → 자동 동기화 사용

macOS: 시스템 환경설정 → 날짜 및 시간 → "날짜와 시간을 자동으로 설정" 활성화

clock skew(시스템 시간 오차)를 수정한 후, 제대로 통합되도록 I2P를 완전히 재시작하세요.

**대역폭 할당 부족**은 성공적인 테스트를 막습니다. router가 테스트 tunnel을 구축하기 위해서는 충분한 용량이 필요합니다. http://127.0.0.1:7657/config에서 설정하세요:

- **최소 동작 가능:** 수신 96 KB/sec, 송신 64 KB/sec
- **권장 표준:** 수신 256 KB/sec, 송신 128 KB/sec  
- **최적 성능:** 수신 512+ KB/sec, 송신 256+ KB/sec
- **공유 비율:** 80% (router가 네트워크에 대역폭을 기여하도록 허용)

대역폭이 낮아도 작동할 수 있지만, 통합 시간은 분 단위에서 시간 단위로 늘어납니다.

부적절한 종료 또는 디스크 오류로 인해 **손상된 netDb**가 발생하면 무한 테스트 루프가 발생합니다. 유효한 피어 데이터가 없으면 router는 테스트를 완료할 수 없습니다:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: `%APPDATA%\I2P\netDb\` 또는 `%LOCALAPPDATA%\I2P\netDb\`의 내용을 삭제하세요

**reseed(초기 피어 확보 절차)을 차단하는 방화벽**은 초기 피어 획득을 방해합니다. bootstrap(초기화 단계) 중, I2P는 HTTPS reseed 서버에서 router 정보를 가져옵니다. 기업/ISP 방화벽이 이러한 연결을 차단할 수 있습니다. 제한적인 네트워크 환경 뒤에서 운영 중이라면 http://127.0.0.1:7657/configreseed 에서 reseed 프록시를 구성하십시오.

## 느린 속도, 시간 초과, 및 tunnel 구축 실패

I2P의 설계는 다중 홉 암호화, 패킷 오버헤드, 경로의 예측 불가능성 때문에 본질적으로 **클리어넷(일반 인터넷) 대비 3-10배 더 느린 속도**를 초래합니다. tunnel 구축은 여러 router를 거치며, 각 router가 지연시간을 더합니다. 이를 이해하면 정상 동작을 문제로 잘못 진단하는 일을 막을 수 있습니다.

**일반적인 성능 기대치:**

- .i2p 사이트 브라우징: 처음에는 페이지 로드에 10-30초, tunnel(익명 통신 경로) 설정 후 더 빨라짐
- I2PSnark를 통한 토렌트: 시더 수와 네트워크 상태에 따라 토렌트당 10-100 KB/sec  
- 대용량 파일 다운로드: 인내 필요 - 메가바이트 크기 파일은 몇 분, 기가바이트 크기는 몇 시간 걸릴 수 있음
- 첫 연결이 가장 느림: tunnel 구축에 30-90초 소요; 이후 연결은 기존 tunnel을 사용

**Tunnel build success rate**는 네트워크 건전성을 나타냅니다. http://127.0.0.1:7657/tunnels에서 확인하세요:

- **60% 초과:** 정상적이고 안정적인 동작
- **40-60%:** 경계 상태, 대역폭 증가 또는 부하 감소를 고려
- **40% 미만:** 문제가 있는 상태 - 대역폭 부족, 네트워크 문제, 또는 부적절한 피어 선택을 의미

**대역폭 할당을 늘리는 것**을 첫 번째 최적화로 삼으세요. 느린 성능의 대부분은 대역폭 부족에서 비롯됩니다. http://127.0.0.1:7657/config에서 한도를 점진적으로 높이고, http://127.0.0.1:7657/graphs에서 그래프를 모니터링하세요.

**DSL/케이블용 (1-10 Mbps 연결):** - 수신: 400 KB/초 - 송신: 200 KB/초 - 공유: 80% - 메모리: 384 MB (wrapper.config 편집)

**고속(10-100+ Mbps 연결)용:** - 수신: 1500 KB/sec   - 송신: 1000 KB/sec - 공유 비율: 80-100% - 메모리: 512-1024 MB - 고려: http://127.0.0.1:7657/configadvanced 에서 참여용 tunnels(트래픽을 중계하는 경로)을 2000-5000으로 늘리기

**tunnel 구성을 최적화**하여 성능을 향상하세요. http://127.0.0.1:7657/i2ptunnel에서 개별 tunnel 설정에 접속하여 각 tunnel을 편집하세요:

- **Tunnel 수량:** 2에서 3-4로 늘리기(더 많은 경로 사용 가능)
- **백업 수량:** 1-2로 설정(tunnel 실패 시 신속한 페일오버)
- **Tunnel 길이:** 기본 3홉은 좋은 균형을 제공함; 2로 줄이면 속도는 향상되지만 익명성은 낮아짐

**네이티브 암호화 라이브러리 (jbigi)**는 순수 Java 암호화보다 5~10배 더 나은 성능을 제공합니다. http://127.0.0.1:7657/logs 에서 로드되었는지 확인하세요 - "jbigi loaded successfully" 또는 "Using native CPUID implementation"을 찾으세요. 없다면:

Linux: 일반적으로 자동으로 감지되어 ~/.i2p/jbigi-*.so에서 로드됩니다 Windows: I2P 설치 디렉터리에 jbigi.dll이 있는지 확인하세요 없으면: 빌드 도구를 설치하고 소스에서 컴파일하거나, 공식 저장소에서 미리 컴파일된 바이너리를 다운로드하세요

**router를 지속적으로 실행 상태로 유지하십시오.** 재시작할 때마다 통합 상태가 초기화되어, tunnel 네트워크와 피어 관계를 다시 구축하는 데 30~60분이 필요합니다. 가동 시간이 길고 안정적인 router는 tunnel 구축 시 우선적으로 선택되어 성능에 긍정적인 피드백 루프가 형성됩니다.

## 높은 CPU 및 메모리 사용량

과도한 리소스 사용은 일반적으로 **불충분한 메모리 할당**, **네이티브 암호 라이브러리 누락**, 또는 **네트워크 참여에 대한 overcommitment(오버커밋)**을 나타냅니다. 적절히 구성된 routers는 활성 사용 중 CPU 10-30%를 사용하고, 할당된 힙의 80% 미만에서 메모리 사용량을 안정적으로 유지해야 합니다.

**메모리 문제는 다음과 같이 나타납니다:** - 상단이 평평한 메모리 그래프(최대치에 고정됨) - 잦은 가비지 컬렉션(급격한 하강이 있는 톱니형 패턴) - 로그에 OutOfMemoryError 발생 - 부하 시 Router가 응답하지 않음 - 리소스 고갈로 인한 자동 종료

**Java 힙 메모리 할당량 늘리기** wrapper.config에서 (완전 종료가 필요함):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**중요:** wrapper.config을 수정한 후, **반드시 완전히 종료해야 합니다** (재시작이 아님), 정상 종료를 위해 11분 동안 기다린 다음, 새로 시작하십시오. Router 콘솔의 "Restart" 버튼은 wrapper 설정을 다시 로드하지 않습니다.

**CPU 최적화에는 네이티브 암호화 라이브러리가 필요합니다.** 순수 Java BigInteger(임의 정밀도 정수) 연산은 네이티브 구현 대비 CPU를 10~20배 더 사용합니다. 시작 시 http://127.0.0.1:7657/logs 에서 jbigi 상태를 확인하세요. jbigi가 없으면 tunnel 구축 및 암호화 작업 동안 CPU 사용률이 50~100%까지 급등합니다.

**참여 tunnel 부하 줄이기** router가 과부하된 경우:

1. http://127.0.0.1:7657/configadvanced 에 접속하세요
2. `router.maxParticipatingTunnels=1000`으로 설정하세요 (기본값 8000)
3. http://127.0.0.1:7657/config 에서 공유 비율을 80%에서 50%로 낮추세요
4. floodfill 모드가 활성화되어 있다면 비활성화하세요: `router.floodfillParticipant=false`

**I2PSnark의 대역폭과 동시 토렌트 수를 제한하세요.** 토렌트는 상당한 시스템 자원을 소모합니다. http://127.0.0.1:7657/i2psnark에서:

- 동시에 활성화된 토렌트를 최대 3~5개로 제한하세요
- "Up BW Limit" 및 "Down BW Limit"을 합리적인 값(각각 50-100 KB/초)으로 설정하세요
- 현재 필요하지 않을 때는 토렌트를 중지하세요
- 수십 개의 토렌트를 동시에 시딩하는 것을 피하세요

**리소스 사용량을 모니터링하세요**: http://127.0.0.1:7657/graphs 에 있는 내장 그래프를 사용하세요. 메모리 그래프는 headroom(여유 공간)이 보여야 하며, flat-top(상단이 평평한 모양)이면 안 됩니다. tunnel 구축 중 발생하는 CPU 급등은 정상이며; 지속적으로 높은 CPU는 구성 문제를 나타냅니다.

**자원이 매우 제한된 시스템** (Raspberry Pi, 구형 하드웨어)에서는 **i2pd** (C++ 구현체)를 대안으로 고려하세요. i2pd는 Java I2P의 350+ MB에 비해 ~130 MB RAM만 필요하고, 유사한 부하에서 CPU 사용률도 Java I2P의 70%에 비해 ~7% 수준입니다. 참고로 i2pd에는 내장 애플리케이션이 없어 외부 도구가 필요합니다.

## I2PSnark 토렌트 문제

I2PSnark가 I2P router 아키텍처와 통합되어 동작하려면, **토렌팅은 전적으로 router tunnel의 상태에 좌우된다**는 점을 이해해야 한다. router가 10개 이상의 활성 피어와 정상 동작하는 tunnel을 확보해 네트워크에 충분히 연동될 때까지 토렌트는 시작되지 않는다.

**0%에서 멈춰 있는 토렌트는 일반적으로 다음을 의미합니다:**

1. **Router가 네트워크에 완전히 통합되지 않음:** I2P 시작 후 토렌트 활동을 기대하기 전에 10~15분 기다리세요
2. **DHT 비활성화됨:** http://127.0.0.1:7657/i2psnark → Configuration → "Enable DHT"에 체크하여 활성화 (버전 0.9.2부터 기본적으로 활성화됨)
3. **유효하지 않거나 죽은 트래커:** I2P 토렌트는 I2P 전용 트래커가 필요합니다 - 클리어넷 트래커는 작동하지 않습니다
4. **불충분한 tunnel 구성:** I2PSnark Configuration → Tunnels 섹션에서 tunnels를 늘리세요

**더 나은 성능을 위해 I2PSnark tunnels 구성하기:**

- 인바운드 tunnels: 3-5 (Java I2P의 기본값은 2, i2pd는 5)
- 아웃바운드 tunnels: 3-5  
- Tunnel 길이: 3홉 (속도를 위해 2로 줄이면 익명성은 낮아짐)
- Tunnel 개수: 3 (일관된 성능 제공)

**필수 I2P 토렌트 트래커** 포함: - tracker2.postman.i2p (기본, 가장 신뢰할 수 있음) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

모든 clearnet(일반 인터넷, non-.i2p) 트래커를 제거하세요 - 이들은 아무런 가치도 제공하지 않고 시간 초과로 끝나는 연결 시도만 만들어냅니다.

트래커와의 통신이 실패할 때 **"Torrent not registered" 오류**가 발생합니다. 토렌트를 마우스 오른쪽 버튼으로 클릭 → "Start"를 선택하면 announce(트래커에 상태를 알리는 요청)를 다시 수행하도록 강제합니다. 문제가 계속되면, I2P로 구성된 브라우저에서 http://tracker2.postman.i2p 로 접속해 트래커에 접근 가능한지 확인하십시오. 죽은 트래커는 동작하는 대체 트래커로 교체해야 합니다.

**피어가 연결되지 않음** 트래커가 정상이어도 다음을 시사합니다: - Router가 방화벽에 막혀 있음 (포트 포워딩을 하면 개선되지만 필수는 아님) - 대역폭이 부족함 (256+ KB/sec 이상으로 늘리기)   - 스웜이 너무 작음 (일부 토렌트는 시더가 1-2명뿐; 인내 필요) - DHT(분산 해시 테이블) 비활성화됨 (트래커 없이 피어를 찾으려면 활성화)

**DHT(분산 해시 테이블)와 PEX(Peer Exchange, 피어 교환)를 활성화** I2PSnark 설정에서. DHT는 트래커에 의존하지 않고 피어를 찾을 수 있게 해줍니다. PEX는 연결된 피어로부터 피어를 발견하여 스웜 탐색을 가속합니다.

**다운로드된 파일 손상**은 I2PSnark의 내장 무결성 검사 덕분에 드물게 발생합니다. 감지된 경우:

1. 토렌트를 마우스 오른쪽 클릭 → "Check"를 선택하면 모든 조각을 강제로 리해시합니다
2. 손상된 토렌트 데이터 삭제(.torrent 파일은 유지)  
3. 마우스 오른쪽 클릭 → "Start"로 조각 검증과 함께 다시 다운로드
4. 손상이 계속되면 디스크 오류를 검사: `chkdsk` (Windows), `fsck` (Linux)

**감시 디렉터리가 작동하지 않음** 문제는 올바른 구성이 필요합니다:

1. I2PSnark 설정 → "Watch directory(감시 디렉터리)": 절대 경로를 지정합니다 (예: `/home/user/torrents/watch`)
2. I2P 프로세스에 읽기 권한이 있는지 확인합니다: `chmod 755 /path/to/watch`
3. .torrent 파일을 watch directory에 놓으면 - I2PSnark가 자동으로 추가합니다
4. "Auto start(자동 시작)" 설정: 토렌트가 추가되면 즉시 시작할지 여부를 선택합니다

**토렌트 사용을 위한 성능 최적화:**

- 동시에 활성 상태인 토렌트 수를 제한하세요: 일반 연결에서는 최대 3~5개
- 중요한 다운로드를 우선시하세요: 우선순위가 낮은 토렌트는 일시적으로 중지하세요
- router 대역폭 할당을 늘리세요: 대역폭이 많을수록 토렌트 성능이 좋아집니다
- 인내심을 가지세요: I2P 토렌트는 clearnet(공개 인터넷) BitTorrent보다 본질적으로 더 느립니다
- 다운로드 후 시딩하세요: 네트워크는 상호성에 기반해 성장합니다

## I2P를 통한 Git 구성 및 문제 해결

I2P를 통한 Git 작업은 SSH/HTTP 액세스를 위해 **SOCKS 프록시 구성** 또는 **전용 I2P tunnels**이 필요하다. Git의 설계는 저지연 연결을 전제로 하므로 I2P의 고지연 아키텍처에서는 어려움이 있다.

**Git에서 I2P SOCKS 프록시를 사용하도록 설정:**

~/.ssh/config를 편집하세요(없다면 생성하세요):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
이는 .i2p 호스트로의 모든 SSH 연결을 I2P의 SOCKS 프록시(포트 4447)를 통해 라우팅합니다. ServerAlive 설정(SSH의 서버 생존 확인 옵션)은 I2P의 지연 시간 동안 연결을 유지합니다.

HTTP/HTTPS git 작업의 경우, git을 전역으로 설정하세요:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
참고: `socks5h` 는 DNS 해석을 프록시를 통해 수행합니다 - .i2p 도메인에 필수적입니다.

**Git SSH용 전용 I2P tunnel 만들기** (SOCKS보다 더 신뢰할 수 있음):

1. http://127.0.0.1:7657/i2ptunnel에 접속
2. "New client tunnel"(터널) → "Standard"
3. 구성:
   - Name: Git-SSH  
   - Type: Client
   - Port: 2222 (Git 액세스를 위한 로컬 포트)
   - Destination: [your-git-server].i2p:22
   - Auto start: Enabled
   - Tunnel count: 3-4 (신뢰성을 위해 더 높게 설정)
4. tunnel을 저장하고 시작
5. SSH가 tunnel을 사용하도록 설정: `ssh -p 2222 git@127.0.0.1`

I2P를 통해 발생하는 **SSH 인증 오류**는 일반적으로 다음과 같은 원인에서 비롯됩니다:

- 키가 ssh-agent에 추가되지 않음: `ssh-add ~/.ssh/id_rsa`
- 잘못된 키 파일 권한: `chmod 600 ~/.ssh/id_rsa`
- Tunnel이 실행 중이 아님: http://127.0.0.1:7657/i2ptunnel 에서 초록색 상태로 표시되는지 확인
- Git 서버에서 특정 키 유형을 요구함: RSA가 실패하면 ed25519 키를 생성

**Git 작업 시간 초과**는 I2P의 지연 특성과 관련이 있습니다:

- Git 타임아웃 늘리기: `git config --global http.postBuffer 524288000` (500MB 버퍼)
- 저속 임계값 늘리기: `git config --global http.lowSpeedLimit 1000` 및 `git config --global http.lowSpeedTime 600` (10분 동안 대기)
- 초기 체크아웃에 shallow clone(최신 커밋만 가져오는 얕은 복제) 사용: `git clone --depth 1 [url]` (최신 커밋만 가져와 더 빠름)
- 활동이 적은 시간대에 복제 수행: 네트워크 혼잡은 I2P 성능에 영향을 줍니다

**느린 git clone/fetch 작업**은 I2P의 아키텍처에 내재된 특성입니다. 100MB 리포지토리는 I2P에서는 30-60분이 걸릴 수 있는 반면, clearnet(일반 인터넷)에서는 몇 초에 불과합니다. 전략:

- 얕은 클론을 사용하세요: `--depth 1`은 초기 데이터 전송량을 크게 줄입니다
- 점진적으로 가져오세요: 전체 클론 대신 특정 브랜치만 가져오세요: `git fetch origin branch:branch`
- I2P 위에서 rsync 사용을 고려하세요: 매우 큰 저장소의 경우 rsync가 더 나은 성능을 보일 수 있습니다
- tunnel 수량을 늘리세요: tunnels의 수가 많을수록 지속적인 대용량 전송에서 더 나은 처리량을 제공합니다

**"Connection refused" 오류**는 tunnel의 잘못된 구성을 나타냅니다:

1. I2P router가 실행 중인지 확인: http://127.0.0.1:7657에서 확인
2. http://127.0.0.1:7657/i2ptunnel에서 tunnel이 활성 상태이며 녹색인지 확인
3. tunnel 테스트: `nc -zv 127.0.0.1 2222` (tunnel이 작동 중이면 연결되어야 함)
4. 대상에 도달 가능한지 확인: 가능하다면 대상의 HTTP 인터페이스에 접속
5. 특정 오류 확인을 위해 http://127.0.0.1:7657/logs에서 tunnel 로그 검토

**I2P를 통한 Git 모범 사례:**

- 안정적인 Git 접속을 위해 I2P router(I2P 노드)를 지속적으로 실행하세요
- 비밀번호 인증 대신 SSH 키를 사용하세요(대화형 프롬프트가 줄어듭니다)
- 일시적인 SOCKS 연결보다 지속적인 tunnels(익명 통신 경로)를 구성하세요
- 더 나은 제어를 위해 직접 I2P git 서버를 운영하는 것을 고려하세요
- 협업자들을 위해 .i2p git 엔드포인트를 문서화해 두세요

## eepsites에 접속하고 .i2p 도메인 이름을 해석하기

사용자가 .i2p 사이트에 접속하지 못하는 가장 흔한 이유는 **잘못된 브라우저 프록시 설정**입니다. I2P 사이트는 I2P 네트워크 내부에서만 존재하며 I2P의 HTTP 프록시를 통해 라우팅되어야 합니다.

**브라우저 프록시 설정을 정확히 구성하세요:**

**Firefox (I2P에 권장됨):**

1. 메뉴 → 설정 → 네트워크 설정 → 설정 버튼
2. "수동 프록시 구성" 선택
3. HTTP 프록시: **127.0.0.1** 포트: **4444**
4. SSL 프록시: **127.0.0.1** 포트: **4444**  
5. SOCKS 프록시: **127.0.0.1** 포트: **4447** (선택 사항, SOCKS 앱용)
6. "SOCKS v5 사용 시 DNS 프록시" 체크
7. 확인을 눌러 저장

**중요한 Firefox about:config 설정:**

`about:config`로 이동하여 다음을 변경하세요:

- `media.peerconnection.ice.proxy_only` = **true** (WebRTC IP 유출을 방지합니다)
- `keyword.enabled` = **false** (.i2p 주소가 검색 엔진으로 리디렉션되는 것을 방지합니다)
- `network.proxy.socks_remote_dns` = **true** (프록시를 통한 DNS)

**Chrome/Chromium 제한 사항:**

Chrome은 애플리케이션별 설정이 아닌 시스템 전체 프록시 설정을 사용합니다. Windows에서: 설정 → "프록시" 검색 → "컴퓨터의 프록시 설정 열기" → HTTP: 127.0.0.1:4444 및 HTTPS: 127.0.0.1:4445를 구성합니다.

더 나은 접근법: 선택적 .i2p 라우팅을 위해 FoxyProxy 또는 Proxy SwitchyOmega 확장 프로그램을 사용하세요.

**"Website Not Found In Address Book" 오류**는 router에 .i2p 도메인의 암호화된 주소가 없음을 의미합니다. I2P는 중앙집중식 DNS 대신 로컬 주소록을 사용합니다. 해결 방법:

**방법 1: jump services(주소록에 사이트 주소를 자동으로 추가해 주는 서비스) 사용** (신규 사이트에 가장 쉬움):

http://stats.i2p 로 이동해 사이트를 검색하세요. addresshelper(주소 도우미) 링크를 클릭하세요: `http://example.i2p/?i2paddresshelper=base64destination`. 브라우저에 "주소록에 저장하시겠습니까?"가 표시되면 확인하여 추가하세요.

**방법 2: 주소록 구독 업데이트:**

1. http://127.0.0.1:7657/dns로 이동하세요 (SusiDNS)
2. "Subscriptions" 탭을 클릭하세요  
3. 활성 구독을 확인하세요 (기본값: http://i2p-projekt.i2p/hosts.txt)
4. 권장 구독을 추가하세요:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. "Update Now"를 클릭하여 구독을 즉시 강제로 업데이트하세요
6. 처리를 위해 5-10분 기다리세요

**방법 3: base32 주소 사용** (사이트가 온라인이면 항상 작동함):

모든 .i2p 사이트에는 Base32 주소가 있습니다: 52개의 무작위 문자 뒤에 .b32.i2p가 붙습니다(예: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Base32 주소는 addressbook(주소록)을 우회하며, router가 직접 암호학적 조회를 수행합니다.

**일반적인 브라우저 설정 실수:**

- HTTP 전용 사이트에서 HTTPS 시도: 대부분의 .i2p 사이트는 HTTP만 사용 - `https://example.i2p`를 시도하면 실패함
- `http://` 접두사 누락: 브라우저가 연결 대신 검색할 수 있음 - 항상 `http://example.i2p`를 사용
- WebRTC(웹 실시간 통신) 활성화됨: 실제 IP 주소가 유출될 수 있음 - Firefox 설정 또는 확장 기능에서 비활성화
- 프록시되지 않은 DNS: 클리어넷(일반 공개 인터넷) DNS는 .i2p를 해석할 수 없음 - DNS 쿼리를 반드시 프록시해야 함
- 잘못된 프록시 포트: HTTP는 4444 (4445가 아님. 이는 클리어넷으로 나가는 HTTPS outproxy(아웃프록시: I2P에서 외부 인터넷으로 나가는 프록시)임)

**Router가 완전히 통합되지 않음** 상태에서는 어떤 사이트에도 접속할 수 없습니다. 충분히 통합되었는지 확인하세요:

1. http://127.0.0.1:7657 에서 "Network: OK" 또는 "Network: Firewalled"로 표시되는지 확인하세요(단, "Network: Testing"은 아님)
2. 활성 피어는 최소 10개 이상(권장 50개 이상)이어야 합니다  
3. "Rejecting tunnels: starting up" 메시지가 없어야 합니다
4. router 시작 후 .i2p에 접속을 기대하기 전에 10~15분을 충분히 기다리세요

**IRC 및 이메일 클라이언트 구성**은 유사한 프록시 패턴을 따릅니다:

**IRC:** 클라이언트는 **127.0.0.1:6668** (I2P의 IRC 프록시 tunnel)에 연결합니다. IRC 클라이언트의 프록시 설정을 비활성화하세요 - localhost:6668로의 연결은 이미 I2P를 통해 프록시됩니다.

**이메일(Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - SSL/TLS 없음 (I2P tunnel이 암호화를 처리함) - postman.i2p 계정 등록 시 발급된 자격 증명

이러한 모든 tunnels가 http://127.0.0.1:7657/i2ptunnel에서 "running"(녹색) 상태로 표시되어야 합니다.

## 설치 실패 및 패키지 문제

패키지 기반 설치(Debian, Ubuntu, Arch)는 **저장소 변경**, **GPG 키 만료**, 또는 **의존성 충돌** 때문에 때때로 실패할 수 있습니다. 최근 버전에서는 공식 저장소가 deb.i2p2.de/deb.i2p2.no(지원 종료)에서 **deb.i2p.net**으로 변경되었습니다.

**Debian/Ubuntu 저장소를 최신 상태로 업데이트:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**GPG 서명 검증 실패**는 저장소 키가 만료되거나 변경될 때 발생합니다:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**패키지 설치 후 서비스가 시작되지 않음**의 가장 흔한 원인은 Debian/Ubuntu의 AppArmor 프로필 문제입니다:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**권한 문제** 패키지로 설치된 I2P에서:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Java 호환성 문제:**

I2P 2.10.0은 **최소 Java 8**을 요구합니다. 구형 시스템에는 Java 7 또는 그 이전 버전이 설치되어 있을 수 있습니다:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Wrapper 구성 오류**로 인해 서비스가 시작되지 않습니다:

Wrapper.config 위치는 설치 방법에 따라 다릅니다:
- 사용자 설치: `~/.i2p/wrapper.config`
- 패키지 설치: `/etc/i2p/wrapper.config` 또는 `/var/lib/i2p/wrapper.config`

일반적인 wrapper.config 문제:

- 경로가 잘못됨: `wrapper.java.command`는 유효한 Java 설치를 가리켜야 합니다
- 메모리 부족: `wrapper.java.maxmemory`가 너무 낮게 설정됨(512 이상으로 늘리세요)
- 잘못된 pidfile(프로세스 ID를 저장하는 파일) 위치: `wrapper.pidfile`은 쓰기 가능한 위치여야 합니다
- wrapper 바이너리 누락: 일부 플랫폼에는 미리 컴파일된 wrapper가 없음(대신 runplain.sh 사용)

**업데이트 실패 및 손상된 업데이트:**

네트워크 중단으로 인해 다운로드 도중 router 콘솔 업데이트가 간헐적으로 실패할 수 있습니다. 수동 업데이트 절차:

1. https://geti2p.net/en/download에서 i2pupdate_X.X.X.zip을 다운로드합니다
2. SHA256 체크섬이 공개된 해시와 일치하는지 확인합니다
3. I2P 설치 디렉터리에 `i2pupdate.zip`으로 복사합니다
4. router를 다시 시작합니다 - 업데이트를 자동으로 감지하고 압축을 해제합니다
5. 업데이트 설치가 완료될 때까지 5-10분 기다립니다
6. http://127.0.0.1:7657에서 새 버전을 확인합니다

**매우 오래된 버전에서의 마이그레이션** (pre-0.9.47)을 현재 버전으로 수행할 때는, 호환되지 않는 서명 키나 제거된 기능 때문에 실패할 수 있습니다. 단계적 업데이트가 필요합니다:

- 0.9.9보다 오래된 버전: 현재 서명을 검증할 수 없음 - 수동 업데이트 필요
- Java 6/7 사용 버전: I2P를 2.x로 업데이트하기 전에 Java를 업그레이드해야 함
- 주요 버전 차이가 큰 경우: 먼저 중간 버전으로 업데이트 (권장 경유점: 0.9.47)

**인스톨러와 패키지 중 언제 사용할지:**

- **패키지(apt/yum):** 서버, 자동 보안 업데이트, 시스템 통합, systemd 관리에 가장 적합
- **설치 프로그램(.jar):** 사용자 수준 설치, Windows, macOS, 맞춤형 설치, 최신 버전 사용에 가장 적합

## 설정 파일 손상 및 복구

I2P의 설정 지속성은 여러 핵심 파일에 의존합니다. 손상은 보통 **부적절한 종료**, **디스크 오류**, 또는 **수동 편집 실수**로 인해 발생합니다. 파일의 용도를 이해하면 전체 재설치 대신 정밀 복구가 가능합니다.

**중요 파일과 그 용도:**

- **router.keys** (516+ 바이트): router의 암호학적 ID - 이 파일을 잃으면 새 ID가 생성됨
- **router.info** (자동 생성): 공개된 router 정보 - 삭제해도 안전하며, 다시 생성됨  
- **router.config** (텍스트): 주요 구성 - 대역폭, 네트워크 설정, 기본 설정
- **i2ptunnel.config** (텍스트): tunnel 정의 - 클라이언트/서버 tunnel, 키, 목적지
- **netDb/** (디렉터리): 피어 데이터베이스 - 네트워크 참여자를 위한 router 정보
- **peerProfiles/** (디렉터리): 피어의 성능 통계 - tunnel 선택에 영향을 줌
- **keyData/** (디렉터리): Destination(목적지) 키(eepsites(익명 웹사이트) 및 서비스용) - 분실하면 주소가 변경됨
- **addressbook/** (디렉터리): 로컬 .i2p 호스트명 매핑

**전체 백업 절차** 변경 전에:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Router.config 손상 징후:**

- 로그에 구문 분석 오류가 있어 router가 시작되지 않음
- 재시작 후 설정이 유지되지 않음
- 예기치 않은 기본값이 나타남  
- 파일을 볼 때 글자가 깨져 보임

**손상된 router.config 복구:**

1. 기존 파일 백업: `cp router.config router.config.broken`
2. 파일 인코딩 확인: BOM 없는 UTF-8이어야 함
3. 구문 확인: 키는 구분자로 `=`를 사용함(`:` 아님), 키 끝에 공백 없어야 함, `#`는 주석에만 사용
4. 흔한 손상: 값에 ASCII가 아닌 문자가 포함, 줄바꿈 방식 문제(CRLF vs LF)
5. 수정 불가한 경우: router.config를 삭제 - router가 기본 router.config를 생성하며 식별자는 유지됨

**보존해야 하는 필수 router.config 설정:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**손실되었거나 유효하지 않은 router.keys** 는 새로운 router identity(라우터 신원)를 생성합니다. 다음의 경우를 제외하면 허용됩니다:

- floodfill 운영 중 (floodfill 상태 상실)
- 공개된 주소로 eepsites 호스팅 (연속성 상실)  
- 네트워크 내에서 확립된 평판

백업이 없으면 복구할 수 없습니다 - 새로 생성: router.keys 삭제, I2P 재시작, 새 식별자 생성.

**중요한 구분:** router.keys (신원) vs keyData/* (서비스). router.keys를 잃으면 router 신원이 변경됩니다. keyData/mysite-keys.dat을 잃으면 eepsite의 .i2p 주소가 변경됩니다 - 주소가 공개되어 있다면 치명적입니다.

**eepsite/서비스 키를 별도로 백업하세요:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**NetDb 및 peerProfiles(피어 프로파일) 손상:**

증상: 활성 피어 0개, tunnel(익명 트래픽 경로)을 구축할 수 없음, 로그에 "Database corruption detected"가 표시됨

안전한 수정(모두 자동으로 reseed(재시드)/rebuild(재구성)됩니다):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
이 디렉터리에는 캐시된 네트워크 정보만 들어 있습니다 - 삭제하면 새로 부트스트랩을 강제하지만 중요한 데이터는 손실되지 않습니다.

**예방 전략:**

1. **항상 정상 종료:** `i2prouter stop`을 사용하거나 router 콘솔의 "Shutdown" 버튼 사용 - 절대 강제 종료하지 말 것
2. **자동 백업:** cron 작업으로 ~/.i2p를 매주 별도 디스크에 백업
3. **디스크 상태 모니터링:** 주기적으로 SMART 상태 확인 - 고장 나는 디스크는 데이터를 손상시킴
4. **충분한 디스크 공간:** 1GB 이상의 여유 공간을 유지 - 디스크가 가득 차면 손상 발생
5. **UPS(무정전 전원장치) 권장:** 쓰기 중 전원 장애는 파일을 손상시킴
6. **중요 구성 파일 버전 관리:** router.config, i2ptunnel.config를 Git 저장소로 관리하면 롤백 가능

**파일 권한은 중요합니다:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## 일반적인 오류 메시지 해설

I2P의 로그 기능은 문제를 정확히 특정할 수 있는 구체적인 오류 메시지를 제공합니다. 이러한 메시지를 이해하면 문제 해결 속도가 빨라집니다.

**"No tunnels available"**는 router가 동작에 필요한 충분한 tunnels을 아직 구축하지 못했을 때 표시됩니다. 이는 시작 후 **처음 5-10분 동안에는 정상**입니다. 15분을 넘어도 지속된다면:

1. http://127.0.0.1:7657에서 활성 피어가 10개 초과인지 확인
2. 대역폭 할당이 충분한지 확인 (최소 128 KB/sec 이상)
3. http://127.0.0.1:7657/tunnels에서 tunnel 성공률을 확인 (40%를 초과해야 함)
4. 로그에서 tunnel 구축 거부 사유를 확인

**"Clock skew detected"** 또는 **"NTCP2 disconnect code 7"**는 시스템 시간이 네트워크 합의 시간과 90초 이상 차이가 있음을 나타냅니다. I2P는 **±60초 정확도**를 요구합니다. 시간 동기화가 어긋난 routers와의 연결은 자동으로 거부됩니다.

즉시 수정:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** 또는 **"Tunnel build timeout exceeded"**는 peer chain(피어 체인)을 통한 tunnel 구축이 타임아웃 시간 제한(일반적으로 60초) 내에 완료되지 않았음을 의미합니다. 원인:

- **느린 피어:** Router가 tunnel에 대해 응답하지 않는 참여자를 선택함
- **네트워크 혼잡:** I2P 네트워크에 높은 부하가 걸림
- **대역폭 부족:** 사용자의 대역폭 제한 때문에 제때 tunnel을 구축하지 못함
- **과부하된 router:** 참여하는 tunnel이 너무 많아 리소스를 소모함

해결 방법: 대역폭을 늘리고, 참여 중인 tunnels 수를 줄이며 (`router.maxParticipatingTunnels`는 http://127.0.0.1:7657/configadvanced에서), 더 나은 피어 선택을 위해 포트 포워딩을 활성화하세요.

**"Router is shutting down"** 또는 **"Graceful shutdown in progress"**는 정상 종료 또는 충돌 복구 중에 표시됩니다. 정상 종료 절차는 router가 tunnel을 닫고 피어들에게 알리며 상태를 영구적으로 저장하기 때문에 **최대 10분**까지 걸릴 수 있습니다.

종료 상태에서 11분을 넘겨 멈춰 있으면 강제로 종료하십시오:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** 는 힙 메모리 고갈을 나타냅니다. 즉각적인 해결책:

1. wrapper.config을 편집하세요: `wrapper.java.maxmemory=512` (또는 더 크게)
2. **완전 종료가 필요합니다** - 재시작만으로는 변경 사항이 적용되지 않습니다
3. 완전 종료될 때까지 11분 기다리세요  
4. router를 새로 시작하세요
5. http://127.0.0.1:7657/graphs 에서 메모리 할당을 확인하세요 - 여유 공간이 보여야 합니다

**관련 메모리 오류:**

- **"GC overhead limit exceeded":** 가비지 컬렉션에 너무 많은 시간이 소모됨 - 힙 크기를 늘리세요
- **"Metaspace(Java 클래스 메타데이터 공간)":** Java 클래스 메타데이터 공간이 고갈됨 - `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`를 추가하세요

**Windows 전용:** Kaspersky Antivirus는 wrapper.config 설정과 관계없이 Java 힙을 512MB로 제한합니다 - Kaspersky Antivirus를 제거하거나 I2P를 검사 제외 목록에 추가하세요.

애플리케이션이 router에 연결을 시도할 때 **"Connection timeout"** 또는 **"I2CP Error - port 7654"**:

1. router가 실행 중인지 확인: http://127.0.0.1:7657 에 접속 시 응답해야 합니다
2. I2CP 포트 확인: `netstat -an | grep 7654` 에서 LISTENING이 표시되어야 합니다
3. localhost 방화벽이 허용하도록 설정: `sudo ufw allow from 127.0.0.1`  
4. 애플리케이션이 올바른 포트를 사용하는지 확인 (I2CP=7654, SAM=7656)

reseed(네트워크 부트스트랩 과정) 중 **"Certificate validation failed"** 또는 **"RouterInfo corrupt"**:

근본 원인: 시계 오차 (먼저 수정), 손상된 netDb, 유효하지 않은 reseed certificates(리시드 인증서)

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Database corruption detected"**는 netDb 또는 peerProfiles에서 디스크 수준의 데이터 손상이 발생했음을 나타냅니다:

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
SMART(S.M.A.R.T., 자가 모니터링/분석/보고 기술) 도구로 디스크 상태를 점검하세요 - 반복적인 손상은 저장장치의 고장 징후일 수 있습니다.

## 플랫폼별 도전 과제

운영 체제가 다르면 권한, 보안 정책, 시스템 통합과 관련해 I2P 배포에서 고유한 과제가 발생한다.

### 리눅스 권한 및 서비스 문제

패키지로 설치된 I2P는 시스템 사용자 **i2psvc** (Debian/Ubuntu) 또는 **i2p** (기타 배포판)로 실행되며, 특정 권한이 필요합니다:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**파일 디스크립터 제한**은 router가 처리할 수 있는 연결 수용 능력에 영향을 줍니다. 기본 제한(1024)은 고대역폭 router에는 불충분합니다:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
Debian/Ubuntu에서 흔한 **AppArmor 충돌**로 인해 서비스가 시작되지 않습니다:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**SELinux 관련 문제** RHEL/CentOS/Fedora에서:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**SystemD(리눅스 초기화 시스템) 서비스 문제 해결:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Windows 방화벽 및 안티바이러스의 간섭

Windows Defender와 타사 백신 제품은 네트워크 동작 패턴 때문에 I2P를 자주 의심 대상으로 표시합니다. 적절한 설정을 통해 보안을 유지하면서 불필요한 차단을 예방할 수 있습니다.

**Windows Defender 방화벽 구성:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
포트 22648을 http://127.0.0.1:7657/confignet에서 확인한 실제 I2P 포트로 바꾸세요.

**Kaspersky Antivirus 특정 문제:** Kaspersky의 "Application Control"은 wrapper.config 설정과 무관하게 Java 힙을 512MB로 제한합니다. 이는 대역폭이 높은 routers에서 OutOfMemoryError(메모리 부족 오류)를 유발합니다.

해결 방법: 1. Kaspersky의 제외 목록에 I2P를 추가: 설정 → 추가 → 위협 및 제외 → 제외 관리 2. 또는 Kaspersky를 제거(I2P 사용을 위해 권장됨)

**타사 안티바이러스 일반 지침:**

- I2P 설치 디렉터리를 예외 목록에 추가  
- %APPDATA%\I2P 및 %LOCALAPPDATA%\I2P를 예외 목록에 추가
- 행위 기반 분석에서 javaw.exe를 제외
- I2P 프로토콜을 방해할 수 있는 "Network Attack Protection"(네트워크 공격 방지) 기능을 비활성화

### macOS Gatekeeper가 설치를 차단함

macOS Gatekeeper(보안 기능)는 서명되지 않은 애플리케이션의 실행을 차단합니다. I2P 설치 프로그램은 Apple Developer ID(애플의 개발자 인증 체계)로 서명되어 있지 않아 보안 경고가 표시됩니다.

**I2P 설치 프로그램용 Gatekeeper(macOS 보안 기능) 우회:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**설치 후 실행** 시에도 여전히 경고가 표시될 수 있습니다:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Gatekeeper를 절대 영구적으로 비활성화하지 마세요** - 다른 애플리케이션에 보안 위험이 됩니다. 파일별 우회만 사용하세요.

**macOS 방화벽 설정:**

1. 시스템 환경설정 → 보안 및 개인 정보 보호 → 방화벽 → 방화벽 옵션
2. "+" 버튼을 클릭하여 앱을 추가합니다  
3. Java 설치 위치로 이동합니다 (예: `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. 추가한 뒤 "들어오는 연결 허용"으로 설정합니다

### Android I2P 애플리케이션 문제

Android 버전 제약과 리소스 제한으로 인해 고유한 도전 과제가 발생합니다.

**최소 요구 사항:** - 현재 버전에는 Android 5.0+ (API level 21+) 필요 - 최소 512MB RAM, 1GB+ 권장   - 앱 및 router 데이터용 100MB 저장 공간 - I2P에 대해 백그라운드 앱 제한 비활성화

**앱이 실행 즉시 강제 종료됩니다:**

1. **Android 버전 확인:** 설정 → 휴대전화 정보 → Android 버전 (5.0 이상이어야 함)
2. **모든 I2P 버전 제거:** 한 종류만 설치하세요:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   여러 개를 동시에 설치하면 충돌합니다
3. **앱 데이터 삭제:** 설정 → 앱 → I2P → 저장공간 → 데이터 삭제
4. **깨끗한 상태에서 재설치**

**배터리 최적화로 인해 router가 종료됨:**

Android는 배터리를 절약하기 위해 백그라운드 앱을 공격적으로 종료합니다. I2P는 배터리 최적화에서 제외해야 합니다:

1. 설정 → 배터리 → 배터리 최적화 (또는 앱 배터리 사용량)
2. I2P 찾기 → 최적화 안 함 (또는 백그라운드 활동 허용)
3. 설정 → 앱 → I2P → 배터리 → 백그라운드 활동 허용 + 제한 해제

**모바일에서의 연결 문제:**

- **Bootstrap(초기 설정 단계)에는 WiFi가 필요합니다:** 초기 reseed(초기 피어 목록 동기화)에서는 상당한 데이터를 다운로드합니다 - 셀룰러가 아니라 WiFi를 사용하세요
- **네트워크 변경:** I2P는 네트워크 전환을 매끄럽게 처리하지 못합니다 - WiFi/셀룰러 전환 후 앱을 재시작하세요
- **모바일용 대역폭:** 셀룰러 데이터 소진을 피하려면 64-128 KB/sec로 보수적으로 설정하세요

**모바일 성능 최적화:**

1. I2P 앱 → 메뉴 → 설정 → 대역폭
2. 적절한 제한값 설정: 셀룰러 사용 시 수신 64 KB/sec, 송신 32 KB/sec
3. participating tunnels 수 줄이기: 설정 → 고급 → Max participating tunnels: 100-200
4. 배터리 절약을 위해 "Stop I2P when screen off" 활성화

**안드로이드에서 토렌트 사용:**

- 동시에 진행되는 토렌트를 최대 2~3개로 제한
- DHT(분산 해시 테이블) 동작을 덜 공격적으로 설정  
- 토렌트에만 WiFi 사용
- 모바일 하드웨어에서는 더 느린 속도를 감수

## Reseed(재시드) 및 bootstrap(부트스트랩) 문제

새로 I2P를 설치하면 네트워크에 참여하기 위해 공개 HTTPS 서버에서 초기 피어 정보를 가져오는 **reseeding**(초기 피어 정보 가져오기)이 필요합니다. reseeding 문제가 발생하면 사용자들은 피어가 0개이고 네트워크에 접속할 수 없는 상태에 갇히게 됩니다.

**신규 설치 직후 "No active peers"**는 일반적으로 reseed(초기 피어 부트스트랩) 실패를 나타냅니다. 증상:

- 알려진 피어: 0이거나 5 미만으로 유지됨
- "Network: Testing" 상태가 15분을 넘어 지속됨
- 로그에 "Reseed failed" 또는 리시드 서버에 대한 연결 오류가 표시됨

**reseed(리시드: 초기 피어 정보 다시 받기)가 실패하는 이유:**

1. **HTTPS 차단 방화벽:** 기업/ISP 방화벽이 reseed server(초기 부트스트랩 서버) 연결을 차단함(포트 443)
2. **SSL 인증서 오류:** 시스템에 최신 루트 인증서가 없음
3. **프록시 필요:** 네트워크가 외부 연결에 HTTP/SOCKS 프록시를 요구함
4. **시계 오차:** 시스템 시간이 잘못되면 SSL 인증서 검증이 실패함
5. **지리적 검열:** 일부 국가/ISP가 알려진 reseed server를 차단함

**수동 reseed(네트워크 초기 피어 목록 다시 가져오기) 강제 실행:**

1. http://127.0.0.1:7657/configreseed 에 접속하세요
2. "Save changes and reseed now"를 클릭하세요 (Reseed: 초기 연결을 위해 피어 정보를 받아오는 과정)  
3. http://127.0.0.1:7657/logs 에서 "Reseed got XX router infos"가 표시되는지 모니터링하세요
4. 처리가 완료될 때까지 5~10분 기다리세요
5. http://127.0.0.1:7657 를 확인하세요 - Known peers가 50+로 증가해야 합니다

**reseed proxy(네트워크 초기 부트스트랩용 프록시) 구성** 제한된 네트워크 환경용:

http://127.0.0.1:7657/configreseed → 프록시 구성:

- HTTP 프록시: [proxy-server]:[port]
- 또는 SOCKS5: [socks-server]:[port]  
- "Use proxy for reseed only" 사용하도록 설정
- 필요한 경우 인증 정보
- 저장하고 reseed(초기 부트스트랩용 피어 정보 다운로드)를 강제로 실행

**대안: reseed(초기 부트스트랩)용 Tor 프록시:**

Tor Browser 또는 Tor 데몬이 실행 중인 경우:

- 프록시 유형: SOCKS5
- 호스트: 127.0.0.1
- 포트: 9050 (기본 Tor SOCKS 포트)
- 활성화 및 reseed(네트워크 부트스트랩)

**su3 파일을 통한 수동 reseed(네트워크 초기 부트스트랩)** (최후의 수단):

자동화된 reseed(리시드: 네트워크 부트스트랩을 위한 초기 피어 정보 획득)가 모두 실패하면, reseed 파일을 별도 경로로 확보하십시오:

1. 제한 없는 연결 상태에서 신뢰할 수 있는 출처로부터 i2pseeds.su3를 다운로드 (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. I2P를 완전히 중지
3. i2pseeds.su3를 ~/.i2p/ 디렉터리로 복사  
4. I2P를 시작 - 파일을 자동으로 추출하고 처리함
5. 처리 후 i2pseeds.su3 삭제
6. http://127.0.0.1:7657에서 피어 수가 증가했는지 확인

**reseed(리시드) 중 SSL 인증서 오류:**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
해결책:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**알려진 피어가 0인 상태로 30분 넘게 멈춰 있음:**

reseed(초기 부트스트랩을 위한 netDb 시드 다운로드 과정)이 완전히 실패했음을 나타냅니다. 문제 해결 순서:

1. **시스템 시간이 정확한지 확인** (가장 흔한 문제 - 가장 먼저 해결)
2. **HTTPS 연결 테스트:** 브라우저에서 https://reseed.i2p.rocks 에 접속해 보세요 - 실패하면 네트워크 문제
3. **I2P 로그 확인** http://127.0.0.1:7657/logs 에서 reseed(네트워크 초기 부트스트랩) 관련 구체적인 오류를 확인
4. **다른 reseed URL 시도:** http://127.0.0.1:7657/configreseed → 사용자 지정 reseed URL 추가: https://reseed-fr.i2pd.xyz/
5. **수동 su3 파일 방법 사용** 자동화된 시도가 모두 소진되었다면

**Reseed servers(리시드 서버) 가끔 오프라인 상태일 수 있음:** I2P에는 여러 개의 하드코딩된 reseed servers가 포함되어 있습니다. 하나가 실패하면 router가 자동으로 다른 reseed servers를 시도합니다. 모든 reseed servers가 전부 실패하는 경우는 극히 드물지만 가능할 수 있습니다.

**현재 활성화된 reseed servers(네트워크 초기 부트스트랩용 서버)** (2025년 10월 기준):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

기본값에 문제가 있는 경우 사용자 지정 URL로 추가하세요.

**검열이 심한 지역의 사용자용:**

초기 reseed(네트워크 부트스트랩)에는 Tor를 통한 Snowflake/Meek bridges 사용을 고려하고, 네트워크에 연결되면 직접 I2P 연결로 전환하세요. 또는 i2pseeds.su3를 스테가노그래피(디지털 은닉 기법), 이메일, 아니면 검열 환경 밖에서 가져온 USB를 통해 확보하세요.

## 추가 도움을 구해야 할 때

이 가이드는 I2P 관련 문제의 대다수를 포괄하지만, 일부 문제는 개발자 검토나 커뮤니티의 전문 지식이 필요합니다.

**다음과 같은 경우 I2P 커뮤니티에 도움을 요청하세요:**

- 모든 문제 해결 단계를 따른 뒤에도 Router가 지속적으로 충돌함
- 메모리 누수로 인해 할당된 힙을 넘어 사용량이 꾸준히 증가함
- 적절한 구성에도 불구하고 tunnel 성공률이 20% 미만으로 유지됨  
- 이 가이드에서 다루지 않은 새로운 오류가 로그에 나타남
- 보안 취약점이 발견됨
- 기능 요청 또는 개선 제안

**도움을 요청하기 전에 진단 정보를 수집하세요:**

1. I2P 버전: http://127.0.0.1:7657 (예: "2.10.0")
2. Java 버전: `java -version` 출력
3. 운영 체제와 버전
4. router 상태: 네트워크 상태, 활성 피어 수, 참여 중인 tunnels
5. 대역폭 구성: 수신/송신 한도
6. 포트 포워딩 상태: 방화벽으로 차단됨(Firewalled) 또는 OK
7. 관련 로그 발췌: http://127.0.0.1:7657/logs 에서 오류가 표시된 마지막 50줄

**공식 지원 채널:**

- **포럼:** https://i2pforum.net (clearnet, 일반 인터넷) 또는 http://i2pforum.i2p (I2P 내에서)
- **IRC:** Irc2P의 #i2p (irc.postman.i2p, I2P를 통해) 또는 irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p 커뮤니티 토론용
- **버그 트래커:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues 확인된 버그 보고용
- **메일링 리스트:** i2p-dev@lists.i2p-projekt.de 개발 관련 질문용

**현실적인 기대치가 중요합니다.** I2P는 근본적인 설계상 clearnet(일반 인터넷)보다 느립니다 - 다중 홉로 암호화된 tunnel(터널)을 이용하는 구조가 고유한 지연을 만들어냅니다. 페이지 로딩에 30초가 걸리고 초당 50 KB의 토렌트 속도가 나오는 I2P router(라우터)는 고장난 것이 아니라 **정상 동작** 중입니다. clearnet 속도를 기대하는 사용자는 설정 최적화와 무관하게 실망하게 될 것입니다.

## 결론

대부분의 I2P 문제는 세 가지 범주에서 비롯됩니다: 부트스트랩 동안의 인내심 부족(10-15분 필요), 불충분한 리소스 할당(512 MB RAM 및 최소 256 KB/sec 대역폭), 또는 잘못 구성된 포트 포워딩. I2P의 분산 아키텍처와 익명성 중심 설계를 이해하면 사용자가 정상적인 동작과 실제 문제를 구분하는 데 도움이 됩니다.

router의 "Firewalled"(방화벽 뒤) 상태는 최적은 아니지만 I2P 사용을 막지는 않습니다 - 네트워크 기여를 제한하고 성능을 약간 저하시킬 뿐입니다. 신규 사용자는 **최적화보다 안정성**을 우선시해야 합니다: 고급 설정을 조정하기 전에 router를 며칠 동안 연속 실행하세요. 가동 시간이 늘어날수록 네트워크 통합이 자연스럽게 개선됩니다.

문제 해결 시에는 항상 기본부터 확인하십시오: 올바른 시스템 시간, 충분한 대역폭, router가 연속으로 실행 중인지, 그리고 10개 이상의 활성 피어. 대부분의 문제는 난해한 구성 매개변수를 조정하기보다 이러한 기본 사항을 점검하면 해결됩니다. 가동 시간이 수일에서 수주에 걸쳐 누적될수록 router가 평판을 쌓고 피어 선택을 최적화하므로, I2P는 인내와 연속 가동에 대해 성능 향상으로 보상합니다.
