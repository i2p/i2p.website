---
title: "I2P-Bote의 부트스트랩을 도와 자원봉사하는 방법"
date: 2019-05-20
author: "idk"
description: "I2P-Bote의 부트스트래핑을 도와주세요!"
categories: ["development"]
---

사람들이 서로 개인적으로 메시지를 주고받도록 돕는 쉬운 방법은, 새로 합류한 I2P-Bote 사용자들이 자신의 I2P-Bote 피어를 부트스트랩(초기 설정)하는 데 쓸 수 있는 I2P-Bote 피어를 운영하는 것입니다. 안타깝게도 지금까지는 I2P-Bote 부트스트랩 피어를 설정하는 과정이 필요 이상으로 난해했습니다. 사실은 매우 간단합니다!

**I2P-bote란 무엇입니까?**

I2P-bote는 i2p 위에 구축된 비공개 메시징 시스템으로, 전송되는 메시지에 대한 정보를 파악하기 더욱 어렵게 만드는 추가 기능들을 갖추고 있습니다. 이러한 특성 덕분에 높은 지연 시간(latency)을 감수하면서도 발신자가 오프라인이 되었을 때 메시지를 대신 전송하는 중앙집중식 릴레이에 의존하지 않고 비공개 메시지를 안전하게 전송할 수 있습니다. 이는 다른 거의 모든 대중적인 비공개 메시징 시스템과 대조적이며, 그러한 시스템들은 양쪽 모두가 온라인 상태여야 하거나 오프라인이 된 발신자를 대신해 메시지를 전달하는 부분적으로 신뢰되는 서비스에 의존합니다.

또는, ELI5(초등학생에게 설명하듯): 이메일과 비슷하게 사용되지만, 이메일의 프라이버시 취약점은 전혀 없습니다.

**1단계: I2P-Bote 설치**

I2P-Bote는 i2p 플러그인으로, 설치가 매우 쉽습니다. 원본 지침은 [bote eepSite, bote.i2p](http://bote.i2p/install/)에서 확인할 수 있지만, clearnet(일반 인터넷)에서 읽고 싶다면, 다음 지침은 bote.i2p에서 제공한 것입니다:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**2단계: 자신의 I2P-Bote 노드의 base64 주소 가져오기**

여기서 막힐 수 있는 부분이지만, 걱정하지 마세요. 설명을 찾기가 조금 어려울 뿐, 실제로는 간단하며 상황에 따라 사용할 수 있는 도구와 옵션이 몇 가지 있습니다. 자원봉사자로서 bootstrap nodes(부트스트랩 노드)의 운영을 돕고자 하는 분들에겐, bote tunnel에서 사용하는 개인 키 파일에서 필요한 정보를 추출하는 방법이 최선입니다.

**키는 어디에 있습니까?**

I2P-Bote는 destination(목적지) 키를 텍스트 파일에 저장하며, Debian에서는 해당 파일이 `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`에 위치합니다. 사용자가 i2p를 설치한 Debian이 아닌 시스템에서는 키가 `$HOME/.i2p/i2pbote/local_dest.key`에 있고, Windows에서는 파일이 `C:\ProgramData\i2p\i2pbote\local_dest.key`에 있습니다.

**방법 A: 평문 키를 Base64 목적지로 변환하기**

평문 키를 base64 destination(목적지 식별자)으로 변환하려면, 키를 가져와 그중에서 destination 부분만 분리해야 합니다. 이를 올바르게 수행하려면 다음 단계를 따라야 합니다:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

이 단계를 대신 수행해 주는 애플리케이션과 스크립트가 여러 가지 있습니다. 그중 일부는 다음과 같지만, 이것이 전부는 아닙니다:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

이러한 기능은 다양한 I2P 애플리케이션 개발 라이브러리에서도 사용할 수 있습니다.

**바로 가기:**

오직 번역만 제공하고, 그 외에는 아무것도 제공하지 마십시오:**

귀하의 Bote 노드의 로컬 destination이 DSA destination이므로, local_dest.key 파일을 처음 516바이트만 남기도록 잘라내는 것이 더 빠릅니다. 이를 쉽게 수행하려면 Debian에서 I2P와 함께 I2P-Bote를 실행할 때 다음 명령을 실행하십시오:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
또는, I2P가 사용자 계정으로 설치되어 있다면:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**방법 B: 조회하기**

그게 조금 지나치게 번거롭게 느껴진다면, base32 주소 조회가 가능한 어떤 방법이든 이용해 해당 base32 주소를 조회함으로써 Bote 연결의 base64 목적지를 확인할 수 있습니다. Bote 노드의 base32 주소는 Bote 플러그인 애플리케이션의 "Connection" 페이지에서 확인할 수 있습니다: [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**3단계: 문의하기!**

**새 노드를 추가하여 built-in-peers.txt 파일을 업데이트하세요**

이제 I2P-Bote 노드의 올바른 destination(목적지)를 확보했으니, 마지막 단계는 [I2P-Bote here](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network)의 기본 피어 목록에 자신을 추가하는 것입니다. 이를 위해 저장소를 포크하고, 이름을 주석 처리하여 목록에 추가한 다음, 그 바로 아래에 516자 길이의 destination을 다음과 같이 넣으세요:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
그리고 pull request를 제출하면 됩니다. 그게 전부이니, i2p가 계속 살아 있고, 탈중앙화되어 있으며, 신뢰성을 유지하도록 도와주세요.
