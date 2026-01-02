---
title: "I2P 개발 로드맵"
description: "I2P 네트워크의 현재 개발 계획과 역사적 성과"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P는 점진적인 개발 모델**을 따르며 약 13주마다 릴리스를 진행합니다. 이 로드맵은 데스크탑과 안드로이드 Java 릴리스를 단일의 안정적인 릴리스 경로로 다룹니다.

**마지막 업데이트:** 2025년 8월

</div>

## 🎯 예정된 릴리스

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### 버전 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
목표: 2025년 12월 초
</div>

- 혼합 PQ MLKEM Ratchet 최종 완료, 기본 활성화 (제안 169)
- Jetty 12, Java 17+ 필요
- PQ 작업 계속 진행 (전송) (제안 169)
- I2CP 조회를 위한 LS 서비스 기록 매개변수 지원 (제안 167)
- 터널별 스로틀링
- 프로메테우스 친화적인 통계 하위 시스템
- SAM Datagram 2/3 지원

</div>

---

## 📦 최근 릴리스

### 2025 릴리스

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**버전 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2025년 9월 8일 출시</span>

- i2psnark UDP 트래커 지원 (제안 160)
- I2CP LS 서비스 기록 매개변수 (일부) (제안 167)
- I2CP 비동기 조회 API
- 혼합 PQ MLKEM Ratchet 베타 (제안 169)
- PQ 작업 계속 진행 (전송) (제안 169)
- 터널 생성 대역폭 매개변수 (제안 168) 2부 (처리)
- 터널별 스로틀링 작업 계속
- 사용되지 않는 전송 ElGamal 코드 제거
- 오래된 SSU2 "활성 스로틀" 코드 제거
- 오래된 통계 로깅 지원 제거
- 통계/그래프 하위 시스템 정리
- 숨김 모드 개선 및 수정

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**버전 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2025년 6월 2일 출시</span>

- Netdb 지도
- Datagram2, Datagram3 구현 (제안 163)
- LS 서비스 기록 매개변수 작업 시작 (제안 167)
- PQ 작업 시작 (제안 169)
- 터널별 스로틀링 작업 계속
- 터널 생성 대역폭 매개변수 (제안 168) 1부 (전송)
- 기본적으로 Linux에서 /dev/random을 PRNG로 사용
- 중복 LS 렌더 코드 제거
- HTML로 변경 로그 표시
- HTTP 서버 스레드 사용량 줄이기
- 자동 플러드필 등록 수정
- 래퍼 업데이트 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**버전 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2025년 3월 29일 출시</span>

- SHA256 손상 버그 수정

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**버전 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2025년 3월 17일 출시</span>

- Java 21+에서 설치 실패 수정
- "루프백" 버그 수정
- 아웃바운드 클라이언트 터널에 대한 터널 테스트 수정
- 공백이 있는 경로에 설치할 때 오류 수정
- 오래된 Docker 컨테이너 및 라이브러리 업데이트
- 콘솔 알림 버블
- SusiDNS 최신 정렬
- Noise에서 SHA256 풀 사용
- 콘솔 다크 테마 수정 및 개선
- .i2p.alt 지원

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**버전 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2025년 2월 3일 출시</span>

- RouterInfo 발행 개선
- SSU2 ACK 효율성 향상
- 중복 릴레이 메시지에 대한 SSU2 처리 개선
- 더 빠른/가변 조회 시간 초과
- LS 만료 개선
- 대칭 NAT 캡 변경
- 더 많은 양식에서 POST 강제
- SusiDNS 다크 테마 수정
- 대역폭 테스트 정리
- 새로운 간 중국어 번역
- 쿠르드 UI 옵션 추가
- 새로운 Jammy 빌드
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 2024 릴리스</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**버전 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2024년 10월 8일 출시</span>

- i2ptunnel HTTP 서버 스레드 사용량 감소
- I2PTunnel의 일반 UDP 터널
- I2PTunnel의 브라우저 프록시
- 웹사이트 마이그레이션
- 노란색으로 변하는 터널 수정
- 콘솔 /netdb 리팩토링

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**버전 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2024년 8월 6일 출시</span>

- 콘솔 내 iframe 크기 문제 수정
- 그래프를 SVG로 변환
- 번들 번역 상태 보고서

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**버전 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2024년 7월 19일 출시</span>

- Netdb 메모리 사용량 줄이기
- SSU1 코드 제거
- i2psnark 임시 파일 누수 및 정지 수정
- i2psnark의 더 효율적인 PEX
- 콘솔 그래프의 JS 새로 고침
- 그래프 렌더링 개선
- Susimail JS 검색
- OBEP에서 더 효율적인 메시지 처리
- 로컬 목적지 I2CP 조회의 효율성 향상
- JS 변수 범위 문제 수정

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**버전 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2024년 5월 15일 출시</span>

- HTTP 잘림 수정
- 대칭 NAT 감지 시 G 기능 공개
- rrd4j 3.9.1-preview로 업데이트

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**버전 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2024년 5월 6일 출시</span>

- NetDB DDoS 완화 조치
- Tor 차단 목록
- Susimail 수정 및 검색
- SSU1 코드 제거 작업 계속
- Tomcat 9.0.88로 업데이트

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**버전 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2024년 4월 8일 출시</span>

- 콘솔 iframe 개선
- i2psnark 대역폭 조절기 재설계
- i2psnark 및 susimail을 위한 Javascript 드래그 앤 드롭
- i2ptunnel SSL 오류 처리 개선
- i2ptunnel 지속적인 HTTP 연결 지원
- SSU1 코드 제거 시작
- SSU2 릴레이 태그 요청 처리 개선
- SSU2 피어 테스트 수정
- Susimail 개선 (로드, 마크다운, HTML 이메일 지원)
- 터널 피어 선택 조정
- RRD4J 3.9로 업데이트
- gradlew 8.5로 업데이트

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**버전 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 2023년 12월 18일 출시</span>

- NetDB 컨텍스트 관리/세그먼트된 NetDB
- 과부하된 라우터의 우선 순위 축소로 혼잡 기능 처리
- Android 헬퍼 라이브러리 부활
- i2psnark 로컬 토렌트 파일 선택기
- NetDB 조회 핸들러 수정
- SSU1 비활성화
- 미래에 발행하는 라우터 금지
- SAM 수정
- susimail 수정
- UPnP 수정

</div>

---

### 2023-2022 릴리스

<details>
<summary>2023-2022 릴리스 확장하려면 클릭</summary>

**버전 2.3.0** — 2023년 6월 28일 출시

- 터널 피어 선택 개선
- 사용자 구성 가능한 차단 목록 만료
- 동일한 출처에서 빠른 조회 폭주 제어
- 재생 감지 정보 누출 수정
- 다중 홈 leaseSets를 위한 NetDB 수정
- 응답으로 수신된 leaseSets를 저장 전에 수신할 때의 NetDB 수정

**버전 2.2.1** — 2023년 4월 12일 출시

- 패키징 수정

**버전 2.2.0** — 2023년 3월 13일 출시

- 터널 피어 선택 개선
- 스트리밍 재생 수정

**버전 2.1.0** — 2023년 1월 10일 출시

- SSU2 수정
- 터널 생성 혼잡 수정
- SSU 피어 테스트 및 대칭 NAT 탐지 수정
- 깨진 LS2 암호화 leaseSets 수정
- SSU 1 비활성화 옵션 (사전)
- 압축 가능한 패딩 (제안 161)
- 새로운 콘솔 피어 상태 탭 추가
- SOCKS 프록시에 torsocks 지원 추가 및 기타 SOCKS 개선 사항 및 수정

**버전 2.0.0** — 2022년 11월 21일 출시

- SSU2 연결 마이그레이션
- SSU2 즉시 acks
- 기본적으로 SSU2 활성화
- i2ptunnel의 SHA-256 다이제스트 프록시 인증
- 최신 AGP를 사용하여 Android 빌드 프로세스 업데이트
- 크로스 플랫폼(데스크탑) I2P 브라우저 자동 구성 지원

**버전 1.9.0** — 2022년 8월 22일 출시

- SSU2 피어 테스트 및 릴레이 구현
- SSU2 수정
- SSU MTU/PMTU 개선
- 소수의 라우터에 대해 SSU2 활성화
- 교착 상태 감지기 추가
- 더 많은 인증서 가져오기 수정
- 라우터 재시작 후 i2psnark DHT 재시작 수정

**버전 1.8.0** — 2022년 5월 23일 출시

- 라우터 패밀리 수정 및 개선
- 소프트 재시작 수정
- SSU 수정 및 성능 개선
- I2PSnark 독립 실행형 수정 및 개선
- 신뢰할 수 있는 패밀리에 대한 Sybil 페널티 방지
- 터널 생성 응답 시간 초과 줄이기
- UPnP 수정
- BOB 출처 제거
- 인증서 가져오기 수정
- Tomcat 9.0.62
- SSU2 지원을 위한 리팩토링 (제안 159)
- SSU2 기본 프로토콜의 초기 구현 (제안 159)
- Android 앱용 SAM 승인 팝업
- i2p.firefox의 사용자 디렉토리 설치 지원 개선

**버전 1.7.0** — 2022년 2월 21일 출시

- BOB 제거
- 새로운 i2psnark 토렌트 편집기
- i2psnark 독립 실행형 수정 및 개선
- NetDB 신뢰성 개선
- 시스템 트레이에 팝업 메시지 추가
- NTCP2 성능 개선
- 첫 번째 홉 실패 시 아웃바운드 터널 제거
- 반복된 클라이언트 터널 구축 실패 후 응답을 위한 탐색 접근 방식으로 재전환
- 터널 동일 IP 제한 복원
- i2ptunnel UDP 지원을 위한 리팩토링 I2CP 포트
- SSU2 작업 계속 진행, 구현 시작 (제안 159)
- I2P 브라우저 프로파일의 Debian/Ubuntu 패키지 생성
- I2P 브라우저 프로파일의 플러그인 생성
- Android 애플리케이션에 대한 문서화 I2P
- i2pcontrol 개선
- 플러그인 지원 개선
- 새로운 로컬 외부 프록시 플러그인
- IRCv3 메시지 태그 지원

</details>

---

### 2021 릴리스

<details>
<summary>2021 릴리스 확장하려면 클릭</summary>

**버전 1.6.1** — 2021년 11월 29일 출시

- ECIES로 라우터 재키 빠르게
- SSU 성능 개선
- SSU 피어 테스트 보안 개선
- 새 설치 마법사에 테마 선택 추가
- SSU2 작업 계속 진행 (제안 159)
- 새로운 터널 빌드 메시지 전송 (제안 157)
- IzPack 설치 프로그램에 자동 브라우저 구성 도구 포함
- 포크 및 실행 플러그인을 관리 가능하게 만들기
- jpackage 설치 프로세스를 문서화
- Go/Java 플러그인 생성 도구 완성 및 문서화
- 자체 서명 HTTPS 리시드를 위한 Reseed 플러그인

**버전 1.5.0** — 2021년 8월 23일 출시

- ECIES로 라우터 재키 빠르게
- SSU2 작업 시작
- 새로운 터널 빌드 메시지 구현
