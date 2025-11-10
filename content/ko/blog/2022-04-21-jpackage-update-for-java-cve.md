---
title: "Java CVE-2022-21449에 대한 Jpackage 업데이트"
date: 2022-04-21
author: "idk"
description: "Java CVE-2022-21449 수정이 포함된 Jpackage 번들이 릴리스됨"
categories: ["release"]
---

## 업데이트 세부 정보

최신 릴리스의 Java 가상 머신을 사용하여 CVE-2022-21449 "Psychic Signatures" 수정이 포함된 새로운 I2P Easy-Install 번들이 생성되었습니다. Easy-Install 번들을 사용하는 사용자는 가능한 한 빨리 업데이트할 것을 권장합니다. 현재 OSX 사용자는 자동으로 업데이트를 받게 되며, Windows 사용자는 다운로드 페이지에서 설치 프로그램을 다운로드하여 일반적인 방식으로 실행하시기 바랍니다.

Linux의 I2P router는 호스트 시스템에서 구성된 Java 가상 머신(JVM)을 사용합니다. 해당 플랫폼의 사용자는 패키지 관리자가 업데이트를 배포할 때까지 취약점을 완화하기 위해 Java 14 미만의 안정적인 Java 버전으로 다운그레이드해야 합니다. 외부 JVM을 사용하는 다른 사용자들은 가능한 한 빨리 JVM을 패치된 버전으로 업데이트해야 합니다.
