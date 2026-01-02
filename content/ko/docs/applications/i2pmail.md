---
title: "I2P Mail (I2P를 통한 익명 이메일)"
description: "I2P 네트워크 내 이메일 시스템 개요 — 역사, 옵션 및 현재 상태"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## 소개

I2P는 내장된 웹메일 클라이언트인 **SusiMail**과 결합된 **Postman's Mail.i2p 서비스**를 통해 이메일 방식의 프라이빗 메시징을 제공합니다. 이 시스템을 통해 사용자는 I2P 네트워크 내부뿐만 아니라 게이트웨이 브리지를 통해 일반 인터넷(clearnet)과의 사이에서도 이메일을 주고받을 수 있습니다.


## Technical Details

**SMTP 서비스**: `localhost:7659` (Postman 제공) **POP3 서비스**: `localhost:7660` **웹메일 접근**: 라우터 콘솔에 내장 `http://127.0.0.1:7657/susimail/`

> **중요**: SusiMail은 이메일을 읽고 보내는 용도로만 사용됩니다. 계정 생성 및 관리는 **hq.postman.i2p**에서 수행해야 합니다.


