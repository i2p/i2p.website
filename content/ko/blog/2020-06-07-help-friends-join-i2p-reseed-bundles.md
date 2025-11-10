---
title: "Reseed Bundles(리시드 번들: 초기 피어 정보 묶음)을 공유하여 친구들이 I2P에 참여하도록 도와주세요"
date: 2020-06-07
author: "idk"
description: "reseed 번들 생성, 교환 및 사용"
categories: ["reseed"]
---

대부분의 새로운 I2P router는 reseed service(부트스트랩을 돕는 시드 제공 서비스)의 도움으로 부트스트래핑하여 네트워크에 합류한다. 그러나 reseed service는 중앙화되어 있으며, I2P 네트워크의 나머지 부분이 탈중앙화되고 차단이 불가능한 연결에 중점을 두고 있다는 점을 고려하면 비교적 차단하기 쉽다. 새로운 I2P router가 부트스트랩하지 못하는 경우, 기존의 I2P router를 사용해 유효한 "Reseed bundle"(리시드 번들)을 생성하여 reseed service 없이 부트스트랩할 수 있다.

정상적으로 I2P에 연결된 사용자는 reseed 파일(초기 부트스트랩용 파일)을 생성하고 비밀 채널 또는 차단되지 않은 채널을 통해 이를 전달함으로써, 차단된 router가 네트워크에 참여하도록 도울 수 있습니다. 실제로 많은 경우 이미 연결된 I2P router는 reseed 차단의 영향을 전혀 받지 않으므로, **주변에 정상적으로 동작하는 I2P router가 있다는 것은 기존 I2P router가 새로운 I2P router에게 숨겨진 부트스트래핑 방법을 제공하여 도울 수 있음을 의미합니다**.

## Reseed Bundle 생성

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## 파일을 통해 Reseed(네트워크 데이터베이스 부트스트랩) 수행

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
