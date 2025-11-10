```markdown
---
title: "I2P Mime Types"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
---

## 개요

일반적인 I2P 파일 형식에 대한 MIME 유형을 정의합니다.
Debian 패키지에 정의를 포함합니다.
.su3 유형 및 가능하면 다른 유형에 대한 핸들러를 제공합니다.

## 동기

브라우저로 다운로드할 때 리시딩 및 플러그인 설치를 용이하게 하기 위해, 
.su3 파일에 대한 MIME 유형과 핸들러가 필요합니다.

프리데스크톱 표준(freedesktop.org standard)을 따라 MIME 정의 파일을 작성하는 방법을 배우고 나면, 
다른 일반적인 I2P 파일 형식에 대한 정의를 추가할 수 있습니다. 
주소록 블록파일 데이터베이스(hostsdb.blockfile)와 같이 일반적으로 다운로드되지 않는 파일에는 
덜 유용하겠지만, 이러한 정의를 사용하면 Ubuntu의 "nautilus"와 같은 그래픽 디렉토리 뷰어를 사용할 때 
파일을 더 잘 식별하고 아이콘화 할 수 있습니다.

MIME 유형을 표준화하면 각 라우터 구현이 적절히 핸들러를 작성할 수 있으며, MIME 정의 파일은 
모든 구현에서 공유할 수 있습니다.

## 설계

프리데스크톱 표준(freedesktop.org standard)을 따르는 XML 소스 파일을 작성하고 
Debian 패키지에 포함합니다. 파일은 "debian/(패키지).sharedmimeinfo"입니다.

모든 I2P MIME 유형은 "application/x-i2p-"로 시작하며, jrobin rrd는 예외입니다.

이 MIME 유형에 대한 핸들러는 애플리케이션별로 지정되며 이곳에서는 명시하지 않습니다.

우리는 또한 정의를 Jetty와 함께 포함하고 리시드 소프트웨어 또는 지침과 함께 포함할 것입니다.

## 명세

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(generic)	application/x-i2p-su3

.su3	(router update)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(reseed)	application/x-i2p-su3-reseed

.su3	(news)		application/x-i2p-su3-news

.su3	(blocklist)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin

## 참조

위에 나열된 모든 파일 형식이 비 Java 라우터 구현에서 사용되는 것은 아닙니다. 
일부는 명확하게 정의되지 않았을 수도 있습니다. 그러나 이곳에 문서화함으로써 
미래의 구현 간 일관성을 가능하게 할 수 있습니다.

".config", ".dat" 및 ".info"와 같은 일부 파일 접미사는 다른 MIME 유형과 겹칠 수 있습니다. 
이는 전체 파일 이름, 파일 이름 패턴 또는 매직 넘버와 같은 추가 데이터를 통해 
구별할 수 있습니다. 예는 zzz.i2p 스레드의 초안 i2p.sharedmimeinfo 파일을 참조하십시오.

중요한 것은 .su3 유형이며, 이 유형은 고유한 접미사와 견고한 매직 넘버 정의를 가지고 있습니다.

## 마이그레이션

해당 사항 없음.
```
