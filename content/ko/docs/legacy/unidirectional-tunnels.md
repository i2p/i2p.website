---
title: "단방향 Tunnels"
description: "I2P의 단방향 tunnel 설계의 역사적 요약."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **역사적 고지:** 이 페이지는 참고를 위해 과거의 “일방향 Tunnels” 논의를 보존합니다. 현재 동작에 대해서는 현행 [tunnel 구현 문서](/docs/specs/implementation/)를 참조하세요.

## 개요

I2P는 **단방향 tunnel**을 구성합니다: 하나의 tunnel은 발신 트래픽을 전달하고, 별도의 tunnel은 수신 응답을 전달합니다. 이 구조는 가장 초기의 네트워크 설계까지 거슬러 올라가며, Tor와 같은 양방향 회로 기반 시스템과의 핵심적인 차별점으로 남아 있습니다. 용어와 구현 세부사항은 [tunnel overview](/docs/overview/tunnel-routing/) 및 [tunnel specification](/docs/specs/implementation/)을 참조하세요.

## 검토

- 단방향 tunnel은 요청과 응답 트래픽을 분리하므로, 어떤 단일한 공모 피어 그룹도 왕복 경로의 절반만 관찰할 수 있다.
- 타이밍 공격은 단일 회로를 분석하는 대신 두 개의 tunnel 풀(아웃바운드와 인바운드)을 교차해야 하므로 상관관계 분석의 난이도가 높아진다.
- 독립적인 인바운드 및 아웃바운드 풀은 routers가 방향별로 지연, 용량, 장애 처리 특성을 조정할 수 있게 한다.
- 단점으로는 피어 관리 복잡성 증가와 신뢰성 있는 서비스 제공을 위해 여러 개의 tunnel 세트를 유지해야 하는 필요가 있다.

## 익명성

Hermann와 Grothoff의 논문 [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf)은 단방향 tunnels에 대한 선행자 공격을 분석하며, 집요한 공격자는 결국 장기간 유지되는 피어를 특정할 수 있음을 시사한다. 커뮤니티 피드백은 이 연구가 공격자의 인내심과 법적 권한에 관한 특정 가정에 의존하고, 양방향 설계에 영향을 미치는 타이밍 공격과 비교하여 이 접근법을 평가하지 않는다고 지적한다. 지속적인 연구와 실무 경험은 단방향 tunnels이 단순한 간과가 아니라 의도적인 익명성 선택임을 계속해서 뒷받침하고 있다.
