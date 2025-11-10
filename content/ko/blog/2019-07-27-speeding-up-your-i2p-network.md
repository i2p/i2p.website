---
title: "I2P 네트워크 속도 향상"
date: 2019-07-27
author: "mhatta"
description: "I2P 네트워크 속도 향상"
categories: ["tutorial"]
---

*이 글은 mhatta의* [미디엄 블로그](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) 를 위해 원래 작성된 자료를 바탕으로 직접 각색한 것입니다 *.* *원글에 대한 공로는 그에게 돌아갑니다. 다음과 같은 부분에서는* *I2P의 오래된 버전을 현재로 언급하던 내용들은 일부 업데이트되었고, 가벼운* *편집을 거쳤습니다. -idk*

시작 직후에는 I2P가 다소 느리게 느껴지는 경우가 많습니다. 그것은 사실이고, 왜 그런지는 우리 모두 잘 알고 있습니다. 본질적으로 프라이버시를 보장하기 위해 [garlic routing(갈릭 라우팅)](https://en.wikipedia.org/wiki/Garlic_routing)은 우리가 익숙한 인터넷 사용 경험에 오버헤드를 추가합니다. 하지만 이는 많은, 혹은 대부분의 I2P 서비스에서 기본적으로 사용자의 데이터가 12개의 홉을 거쳐야 함을 의미합니다.

![온라인 익명성 도구 분석](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

또한 Tor와 달리, I2P는 주로 폐쇄형 네트워크로 설계되었습니다. I2P 내부의 [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) 또는 다른 리소스에는 쉽게 접근할 수 있지만, I2P를 통해 [clearnet](https://en.wikipedia.org/wiki/Clearnet_(networking))(일반 인터넷) 웹사이트에 접근하도록 되어 있지는 않습니다. clearnet에 접근하기 위해 [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network))의 exit 노드와 유사한 I2P "outproxies"(외부 프록시)가 몇 개 존재하지만, clearnet으로 나가는 것은 이미 6홉 인바운드, 6홉 아웃바운드로 구성된 연결에 실질적으로 *또 하나의* 홉을 추가하는 셈이기 때문에 대부분 사용하기에 매우 느립니다.

몇 버전 전까지만 해도, 많은 I2P router 사용자들이 자신의 router의 대역폭 설정을 구성하는 데 어려움을 겪었기 때문에 이 문제는 더 다루기 어려웠습니다. 할 수 있는 모든 사람이 시간을 내어 자신의 대역폭 설정을 제대로 조정하면, 여러분의 연결뿐만 아니라 I2P 네트워크 전체도 개선됩니다.

## 대역폭 제한 조정

I2P는 피어 투 피어 네트워크이므로, 다른 피어들과 네트워크 대역폭의 일부를 공유해야 합니다. 얼마나 공유할지는 "I2P Bandwidth Configuration"(I2P Router Console의 "Applications and Configuration" 섹션에 있는 "Configure Bandwidth" 버튼, 또는 http://localhost:7657/config)에서 선택할 수 있습니다.

![I2P 대역폭 설정](https://geti2p.net/images/blog/bandwidthmenu.png)

공유 대역폭 제한이 48 KBps로 매우 낮게 표시된다면, 기본값에서 공유 대역폭을 조정하지 않았을 가능성이 있습니다. 이 블로그 게시물이 각색된 자료의 원저자가 지적했듯이, I2P에는 사용자가 자신의 연결에 문제가 생기지 않도록 조정하기 전까지 매우 낮은 기본 공유 대역폭 제한이 설정되어 있습니다.

그러나 많은 사용자가 어떤 대역폭 설정을 조정해야 하는지 정확히 알지 못할 수 있으므로, [I2P 0.9.38 릴리스](https://geti2p.net/en/download)에서는 New Install Wizard(새 설치 마법사)를 도입했습니다. 여기에는 Bandwidth Test(대역폭 테스트)가 포함되어 있으며, M-Lab의 [NDT](https://www.measurementlab.net/tests/ndt/) 덕분에 대역폭을 자동으로 측정하고 I2P의 대역폭 설정을 이에 맞게 조정합니다.

마법사를 다시 실행하고 싶다면, 예를 들어 서비스 제공업체가 변경되었거나 0.9.38 버전 이전에 I2P를 설치했기 때문이라면, 'Help & FAQ' 페이지의 'Setup' 링크에서 다시 실행하거나, http://localhost:7657/welcome 에서 마법사에 직접 접속하면 됩니다.

!["Setup"을 찾을 수 있나요?](https://geti2p.net/images/blog/sidemenu.png)

마법사를 사용하는 것은 간단하며, 단순히 "Next"를 계속 클릭하면 됩니다. 가끔 M-Lab에서 선택한 측정 서버가 다운되어 테스트가 실패할 수 있습니다. 이런 경우에는 "Previous"를 클릭하고(웹 브라우저의 "back" 버튼은 사용하지 마세요), 그런 다음 다시 시도해 보세요.

![대역폭 테스트 결과](https://geti2p.net/images/blog/bwresults.png)

## I2P를 상시 실행하기

대역폭을 조정한 이후에도 연결이 여전히 느릴 수 있습니다. 말씀드렸듯이, I2P는 P2P 네트워크입니다. 다른 피어들이 사용자의 I2P router를 발견하고 I2P 네트워크에 통합하는 데에는 시간이 걸립니다. I2P router가 충분히 오랫동안 가동되지 않아 네트워크에 잘 통합되지 못했거나, 정상 종료하지 않고 자주 종료한다면, 네트워크 속도는 상당히 느린 상태로 남을 수 있습니다. 반대로, I2P router를 오래 연속으로 실행할수록 연결은 더 빠르고 안정적이 되며, 사용자의 대역폭 기여분도 네트워크에서 더 많이 활용됩니다.

그러나 많은 사람들은 자신의 I2P router를 계속 가동 상태로 유지하지 못할 수도 있습니다. 이러한 경우에도 VPS와 같은 원격 서버에서 I2P router를 실행한 다음 SSH 포트 포워딩을 사용할 수 있습니다.
