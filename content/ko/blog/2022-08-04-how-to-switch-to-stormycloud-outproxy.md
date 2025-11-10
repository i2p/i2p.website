---
title: "StormyCloud 아웃프록시 서비스로 전환하는 방법"
date: 2022-08-04
author: "idk"
description: "StormyCloud Outproxy(아웃프록시) 서비스로 전환하는 방법"
categories: ["general"]
---

## StormyCloud Outproxy(외부 프록시) 서비스로 전환하는 방법

**새롭고 전문적인 Outproxy(아웃프록시)**

수년간 I2P는 단일 기본 outproxy(아웃프록시)인 `false.i2p`가 이를 담당해 왔으나, 그 신뢰성은 점점 저하되어 왔습니다. 일부 공백을 메우기 위해 여러 경쟁 서비스가 등장했지만, 대부분은 전체 I2P 구현의 모든 클라이언트를 기본값으로 담당하겠다고 자원할 수는 없습니다. 그러나 Tor 출구 노드를 운영하는 전문 비영리 조직인 StormyCloud가 새롭고 전문적인 outproxy 서비스를 시작했고, 이는 I2P 커뮤니티 구성원들의 테스트를 거쳤으며 다가오는 릴리스에서 새로운 기본 outproxy가 될 것입니다.

**StormyCloud는 누구인가**

그들의 말에 따르면, StormyCloud는:

> StormyCloud Inc의 사명: 인터넷 접근을 보편적 인권으로서 수호하는 것이다. 그렇게 함으로써 이 단체는 사용자의 전자적 프라이버시를 보호하고 정보에 대한 제한 없는 접근을 촉진하여 국경을 넘어 사상의 자유로운 교류가 이루어지도록 하고, 이를 통해 공동체를 구축한다. 이는 인터넷이 세계에 긍정적인 변화를 이루는 데 사용할 수 있는 가장 강력한 도구이기 때문에 필수적이다.

> 하드웨어: 당사는 모든 하드웨어를 직접 소유하고 있으며, 현재 Tier 4 데이터 센터에서 코로케이션 중입니다. 현재 10GBps 업링크를 사용하고 있고, 큰 변경 없이 40GBps로 업그레이드할 수 있는 옵션이 있습니다. 또한 자체 ASN(자율 시스템 번호)과 IP 대역(IPv4 및 IPv6)을 보유하고 있습니다.

StormyCloud에 대해 더 알아보려면 그들의 [웹사이트](https://www.stormycloud.org/)를 방문하십시오.

또는 [I2P](http://stormycloud.i2p/)에서 방문하세요.

**Switching to the StormyCloud Outproxy on I2P**

StormyCloud outproxy(아웃프록시)로 *오늘* 전환하려면 [the Hidden Services Manager](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0)를 방문하십시오. 해당 페이지에서 **Outproxies** 및 **SSL Outproxies** 값을 `exit.stormycloud.i2p`로 변경하십시오. 이 작업을 완료한 후, 페이지 하단으로 스크롤하여 "Save" 버튼을 클릭하십시오.

**StormyCloud에게 감사드립니다**

I2P 네트워크에 고품질 outproxy 서비스(클리어넷으로 나가는 프록시 서비스)를 자원하여 제공해 주신 StormyCloud에 감사드립니다.
