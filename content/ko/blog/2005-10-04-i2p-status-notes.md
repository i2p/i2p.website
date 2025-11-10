---
title: "2005-10-04자 I2P 현황 노트"
date: 2005-10-04
author: "jr"
description: "피어 3-400개를 달성한 0.6.1.1 릴리스 성공, i2phex 포크 통합 노력, 그리고 pet names(사용자 지정 별칭) 및 scheduled pulls(예약된 pull 작업)을 포함한 Syndie 자동화 진척 상황을 다루는 주간 업데이트"
categories: ["status"]
---

안녕하세요 여러분, 우리의 주간 상태 노트 시간이에요 (여기서 환호해주세요)

* Index

1) 0.6.1.1 2) i2phex 3) syndie 4) ???

* 1) 0.6.1.1

평소 공지 채널에 알린 바와 같이, 0.6.1.1이 며칠 전에 공개되었고, 현재까지 보고는 긍정적입니다. 네트워크는 안정적으로 3-400개의 알려진 피어로 성장했으며, 성능도 꽤 좋은 편이지만 CPU 사용량이 다소 증가했습니다. 이는 유효하지 않은 IP 주소가 잘못 허용되도록 하는 오랫동안 존재해 온 버그로 인해 필요 이상으로 높은 churn(노드 변동)이 발생한 탓일 가능성이 큽니다. 0.6.1.1 이후의 CVS 빌드에는 이에 대한 수정과 기타 변경이 포함되어 있으므로, 아마 이번 주 후반에 0.6.1.2를 내놓을 것 같습니다.

* 2) i2phex

i2phex와 legion의 포크에 관한 논의를 여러 포럼에서 보신 분들도 계시겠지만, 저와 legion은 추가로 소통을 이어왔으며 두 프로젝트를 다시 하나로 병합하는 작업을 진행하고 있습니다. 이에 대한 추가 정보는 준비되는 대로 알려드리겠습니다.

게다가 redzara는 현재 phex 릴리스와 i2phex를 병합하는 작업에 매진하고 있고, striker가 몇 가지 추가 개선 사항도 내놓았으므로, 곧 흥미로운 것들이 나올 예정이다.

* 3) syndie

Ragnarok has been working away on syndie the last few days, integrating syndie's pet name database with the router's, as well as automating the syndication with scheduled pulls from selected remote archives. The automation part is done, and while there's some UI work left, its in pretty good shape!

* 4) ???

요즘에도 여러 가지 일이 많이 진행되고 있습니다. 새 기술 소개 문서 작업, IRC 마이그레이션(이전), 그리고 웹사이트 개편 등이 포함됩니다. 제기하고 싶은 안건이 있으신 분은 몇 분 후 열릴 회의에 잠깐 들러 인사해 주세요!

=jr
