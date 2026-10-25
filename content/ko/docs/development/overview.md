---
title: "기술 문서 색인"
description: "I2P 기술 문서 색인"
slug: "overview"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
aliases:
  - "/ko/docs/develop/overview"
  - "/ko/docs/develop/overview/"
---


## 개요 {#overview}

- [기술 소개](/docs/overview/intro)
- [덜 기술적인 소개](/docs/overview/intro/)
- [위협 모델 및 분석](/docs/overview/threat-model)
- [다른 익명 네트워크와의 비교](/docs/overview/comparison)
- [프로토콜 스택 차트](/docs/development/protocol-stack)
- [I2P에 관한 논문](/papers/)
- [프레젠테이션, 기사, 튜토리얼, 비디오 및 인터뷰](/about/media/)
- [보이지 않는 인터넷 프로젝트(I2P) 프로젝트 개요 - 2003년 8월 28일 (PDF)](/docs/historical/i2p_philosophy.pdf)


## 응용 계층 주제 {#applications}

- [애플리케이션 개발 개요 및 가이드](/docs/development/applications)
- [명명 및 주소록](/docs/overview/naming)
- [주소록 구독 피드 명령](/docs/specs/subscription)
- [플러그인 개요](/docs/guides/plugins)
- [플러그인 사양](/docs/specs/plugin)
- [관리되는 클라이언트](/docs/applications/managed-clients)
- [애플리케이션에 라우터 임베딩](/docs/applications/embedding)
- [I2P를 통한 비트토렌트](/docs/applications/bittorrent)
- [I2PControl 플러그인 API](/docs/api/i2pcontrol)
- [hostsdb.blockfile 형식](/docs/specs/blockfile)
- [구성 파일 형식](/docs/specs/configuration)


## 응용 계층 API 및 프로토콜 {#api}

- [I2PTunnel](/docs/api/i2ptunnel)
- [I2PTunnel 구성](/docs/specs/configuration)
- [SOCKS 프록시](/docs/api/socks)
- [SAMv3 프로토콜](/docs/api/samv3)
- [SAM 프로토콜](/docs/legacy/sam) (사용 중단)
- [SAMv2 프로토콜](/docs/legacy/samv2) (사용 중단)
- [BOB 프로토콜](/docs/legacy/bob) (사용 중단)


## 종단 간 전송 API 및 프로토콜 {#transport-api}

- [스트리밍 프로토콜 개요](/docs/api/streaming)
- [스트리밍 프로토콜 사양](/docs/specs/streaming)
- [데이터그램](/docs/api/datagrams)
- [데이터그램 사양](/docs/specs/datagrams)


## 클라이언트-라우터 인터페이스 API 및 프로토콜 {#i2cp}

- [I2CP 개요](/docs/specs/i2cp)
- [I2CP 사양](/docs/specs/i2cp)
- [공통 데이터 구조 사양](/docs/specs/common-structures)


## 종단 간 암호화 {#encryption}

- [목적지용 ECIES-X25519-AEAD-Ratchet 암호화](/docs/specs/ecies)
- [하이브리드 ECIES-X25519 암호화](/docs/specs/ecies-hybrid)
- [라우터용 ECIES-X25519 암호화](/docs/specs/ecies-routers)
- [ElGamal/AES+SessionTag 암호화](/docs/specs/elgamal-aes)
- [ElGamal 및 AES 암호화 세부사항](/docs/specs/cryptography)


## 네트워크 데이터베이스 {#netdb}

- [네트워크 데이터베이스 개요, 세부사항 및 위협 분석](/docs/overview/network-database)
- [암호화 해시](/docs/specs/cryptography#hashes)
- [암호화 서명](/docs/specs/cryptography#signatures)
- [Red25519 서명](/docs/specs/red25519)
- [라우터 리시드 사양](/docs/misc/reseed)
- [암호화된 리스셋용 Base32 주소](/docs/specs/b32encrypted)


## 라우터 메시지 프로토콜 {#i2np}

- [I2NP 개요](/docs/specs/i2np)
- [I2NP 사양](/docs/specs/i2np)
- [공통 데이터 구조 사양](/docs/specs/common-structures)
- [암호화된 리스셋 사양](/docs/specs/encryptedleaseset)


## 터널 {#tunnels}

- [피어 프로파일링 및 선택](/docs/overview/peer-selection)
- [터널 라우팅 개요](/docs/overview/tunnel-routing)
- [갈릭 라우팅 및 용어](/docs/overview/garlic-routing)
- [터널 구축 및 암호화](/docs/specs/tunnel-creation)
- [빌드 요청 암호화를 위한 ElGamal/AES](/docs/specs/elgamal-tunnel-creation)
- [ElGamal 및 AES 암호화 세부사항](/docs/specs/cryptography)
- [터널 구축 사양 (ElGamal)](/docs/specs/tunnel-creation)
- [터널 구축 사양 (ECIES-X25519)](/docs/specs/tunnel-creation-ecies)
- [저수준 터널 메시지 사양](/docs/specs/tunnel-message)
- [단방향 터널](/docs/legacy/unidirectional)
- [I2P 익명 네트워크에서의 피어 프로파일링 및 선택 - 2009 (PDF)](/docs/historical/I2P-PET-CON-2009.1.pdf)


## 전송 계층 {#transports}

- [전송 계층 개요](/docs/overview/transport)
- [NTCP2 사양](/docs/specs/ntcp2)
- [SSU2 사양](/docs/specs/ssu2)
- [NTCP (레거시)](/docs/legacy/ntcp)
- [SSU 개요 (레거시)](/docs/legacy/ssu-overview)


## 기타 라우터 주제 {#router}

- [라우터 소프트웨어 업데이트](/docs/specs/updates)
- [라우터 리시드 사양](/docs/misc/reseed)
- [성능](/docs/overview/performance)
- [구성 파일 형식](/docs/specs/configuration)
- [GeoIP 파일 형식](/docs/legacy/geoip)
- [I2P에서 사용하는 포트](/docs/overview/ports)


## 개발자 가이드 및 리소스 {#develop}

- [신규 개발자 가이드](/docs/development/new-developers)
- [신규 번역자 가이드](/docs/development/new-translators)
- [개발자 가이드라인](/docs/development/dev-guidelines)
- [제안](/proposals/)
- [애플리케이션에 라우터 임베딩](/docs/applications/embedding)
- [리시드 서버 설정 방법](/docs/guides/reseed-server)
- [I2P에서 사용하는 포트](/docs/overview/ports)
- [프로젝트 로드맵](/get-involved/roadmap/)
- [고대 invisiblenet I2P 문서 - 2003](/docs/historical/)
