---
title: "엄격한/제한적인 국가"
description: "I2P가 라우팅 또는 익명성 도구에 제한이 있는 관할권에서 작동하는 방식 (Hidden Mode 및 strict list)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: 문서
reviewStatus: "needs-review"
---

I2P의 이 구현체(이 사이트에서 배포되는 Java 구현체)는 법률상 타인을 위한 라우팅 참여가 제한될 수 있는 지역에서 router 동작을 조정하기 위해 사용되는 "Strict Countries List"를 포함하고 있습니다. I2P 사용을 금지하는 관할권에 대해서는 알지 못하지만, 일부 국가에서는 트래픽 중계에 대한 광범위한 금지 조항이 있습니다. "strict" 국가에 있는 것으로 보이는 router는 자동으로 Hidden 모드로 설정됩니다.

프로젝트는 이러한 결정을 내릴 때 시민 및 디지털 권리 단체의 연구를 참조합니다. 특히 Freedom House의 지속적인 연구가 우리의 선택에 정보를 제공합니다. 일반적인 지침은 시민 자유(CL) 점수가 16점 이하이거나 인터넷 자유 점수가 39점 이하(자유롭지 않음)인 국가를 포함하는 것입니다.

## 히든 모드 요약

라우터가 Hidden 모드로 설정되면 동작 방식에서 세 가지 주요 변화가 발생합니다:

- netDb에 RouterInfo를 게시하지 않습니다.
- 중계 터널(participating tunnels)을 수락하지 않습니다.
- 같은 국가의 라우터에 대한 직접 연결을 거부합니다.

이러한 방어 메커니즘은 라우터를 안정적으로 열거하기 어렵게 만들고, 타인의 트래픽을 중계하는 것에 대한 지역 규제를 위반할 위험을 줄입니다.

## 엄격한 국가 목록 (2024년 기준)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
엄격한 목록에 국가를 추가하거나 제거해야 한다고 생각하시면, 이슈를 등록해 주세요: https://i2pgit.org/i2p/i2p.i2p/

참고: Freedom House – https://freedomhouse.org/
