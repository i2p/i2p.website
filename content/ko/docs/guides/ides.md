---
title: "IDE를 사용한 I2P 개발"
description: "Gradle과 번들 프로젝트 파일을 사용하여 I2P 개발을 위한 Eclipse 및 NetBeans 설정"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

<p> 메인 I2P 개발 브랜치(<code>i2p.i2p</code>)는 개발자들이 자바 개발에 일반적으로 사용되는 두 가지 IDE인 Eclipse와 NetBeans를 쉽게 설정할 수 있도록 구성되어 있습니다. </p>

<h2>Eclipse</h2>

<p> 주요 I2P 개발 브랜치(<code>i2p.i2p</code> 및 이로부터 파생된 브랜치)에는 Eclipse에서 브랜치를 쉽게 설정할 수 있도록 <code>build.gradle</code>이 포함되어 있습니다. </p>

<ol> <li> 최신 버전의 Eclipse가 설치되어 있는지 확인하세요. 2017년 이후 버전이면 충분합니다. </li> <li> I2P 브랜치를 특정 디렉토리(예: <code>$HOME/dev/i2p.i2p</code>)에 체크아웃하세요. </li> <li> "File → Import..."를 선택한 다음 "Gradle" 아래에서 "Existing Gradle Project"를 선택하세요. </li> <li> "Project root directory:"에는 I2P 브랜치를 체크아웃한 디렉토리를 선택하세요. </li> <li> "Import Options" 대화상자에서 "Gradle Wrapper"를 선택하고 Continue를 누르세요. </li> <li> "Import Preview" 대화상자에서 프로젝트 구조를 검토할 수 있습니다. "i2p.i2p" 아래에 여러 프로젝트가 표시되어야 합니다. "Finish"를 누르세요. </li> <li> 완료! 이제 작업 공간에 I2P 브랜치 내의 모든 프로젝트가 포함되어 있으며, 빌드 종속성이 올바르게 설정되어 있어야 합니다. </li> </ol>

<h2>NetBeans</h2>

<p> 주요 I2P 개발 브랜치(<code>i2p.i2p</code> 및 여기서 파생된 브랜치)에는 NetBeans 프로젝트 파일이 포함되어 있습니다. </p>

<!-- 콘텐츠는 최소한으로 유지하고 원본에 가깝게 유지; 나중에 업데이트 예정. -->
