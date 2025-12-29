---
title: "암호화된 LeaseSets로 I2P 역량을 한 단계 끌어올리세요"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "I2P가 Hidden Services(숨김 서비스)를 강조한다고들 합니다. 이에 대한 한 가지 해석을 검토합니다."
categories: ["general"]
---

## 암호화된 LeaseSets로 I2P 실력을 한 단계 끌어올리세요

과거에는 I2P가 은닉 서비스 지원을 강조한다고들 했으며, 이는 여러 면에서 사실입니다. 그러나 이것이 사용자, 개발자, 그리고 은닉 서비스 관리자에게 의미하는 바는 항상 같지 않습니다. Encrypted LeaseSets(LeaseSet: 목적지에 도달하기 위한 정보를 담은 I2P 데이터 구조)과 그 사용 사례는 I2P가 은닉 서비스를 더 유연하게 만들고 관리하기 쉽게 만드는 방식, 그리고 I2P가 은닉 서비스 개념을 확장하여 잠재적으로 흥미로운 사용 사례에 보안상 이점을 제공하는 방식을 보여 주는 독특하고 실용적인 창을 제공합니다.

## LeaseSet이란 무엇인가요?

숨김 서비스를 생성하면 I2P NetDB에 "LeaseSet"이라고 불리는 것을 발행합니다. "LeaseSet"은 가장 단순하게 말해, 다른 I2P 사용자들이 I2P 네트워크에서 당신의 숨김 서비스가 "어디"에 있는지 찾아내는 데 필요한 것입니다. 여기에는 숨김 서비스에 도달하는 데 사용할 수 있는 tunnel들을 식별하는 "Leases"와, 클라이언트가 그쪽으로 메시지를 암호화해 보내게 되는 destination(목적지)의 공개 키가 포함됩니다. 이러한 유형의 숨김 서비스는 주소를 가진 누구나 접근할 수 있으며, 이는 현재로서는 가장 일반적인 사용 사례일 것입니다.

하지만 때로는 자신의 숨겨진 서비스가 누구에게나 접근 가능하도록 허용하고 싶지 않을 수도 있습니다. 일부 사람들은 숨겨진 서비스를 가정용 PC의 SSH 서버에 접속하는 수단으로 사용하거나, IoT 장치들을 서로 연결해 하나의 네트워크를 구성하기 위해 사용합니다. 이러한 경우에는 숨겨진 서비스를 I2P 네트워크의 모든 사용자에게 접근 가능하게 만들 필요가 없고, 오히려 역효과를 낳을 수도 있습니다. 여기에서 "암호화된 LeaseSets(서비스의 접근 경로 정보를 담은 메타데이터)"가 중요한 역할을 합니다.

## 암호화된 LeaseSets: 매우 숨겨진 서비스

암호화된 LeaseSets는 NetDB에 암호화된 형태로 게시되는 LeaseSets로서, 클라이언트가 해당 LeaseSet을 복호화하는 데 필요한 키를 가지고 있지 않다면 어떤 Lease나 공개키도 보이지 않습니다. 사용자가 키를 공유한 클라이언트(PSK Encrypted LeaseSets의 경우) 또는 자신의 키를 사용자와 공유한 클라이언트(DH Encrypted LeaseSets의 경우)만 destination(목적지)을 볼 수 있으며, 그 외에는 아무도 볼 수 없습니다.

I2P는 암호화된 LeaseSet을 위한 여러 가지 전략을 지원합니다. 어떤 것을 사용할지 결정할 때는 각 전략의 핵심 특성을 이해하는 것이 중요합니다. 암호화된 LeaseSet이 "Pre-Shared Key(PSK)" 전략을 사용할 경우, 서버가 키(또는 여러 키)를 생성하고 서버 운영자가 이를 각 클라이언트와 공유합니다. 물론 이러한 교환은 오프밴드(out-of-band)로 이뤄져야 하며, 예를 들어 IRC에서의 교환을 통해 수행될 수 있습니다. 이 방식의 암호화된 LeaseSet은 비밀번호로 Wi‑Fi에 로그인하는 것과 비슷합니다. 다만, 여러분이 로그인하는 대상은 Hidden Service(숨김 서비스)입니다.

Encrypted LeaseSet이 'Diffie-Hellman(DH)' 전략을 사용한다면, 키는 클라이언트에서 생성됩니다. Diffie-Hellman 클라이언트가 Encrypted LeaseSet을 사용하는 destination(목적지)에 연결할 때, 먼저 서버 운영자와 자신의 키를 공유해야 합니다. 그 다음 서버 운영자가 DH 클라이언트를 승인할지 결정합니다. 이 버전의 Encrypted LeaseSets는 `authorized_keys` 파일을 사용하는 SSH와 비슷합니다. 단, 여러분이 로그인하는 곳은 은닉 서비스입니다.

LeaseSet을 암호화하면, 권한 없는 사용자가 귀하의 목적지에 연결하는 것을 불가능하게 만들 뿐만 아니라, 권한 없는 방문자가 I2P 히든 서비스의 실제 목적지를 알아내는 것조차 불가능하게 만듭니다. 일부 독자들은 아마도 이미 자신만의 암호화된 LeaseSet 사용 사례를 떠올렸을 것입니다.

## 암호화된 LeaseSets를 사용하여 router 콘솔에 안전하게 접근하기

일반적으로, 서비스가 사용자의 장치에 관한 더 복잡한 정보에 접근할수록, 그 서비스를 인터넷에, 나아가 I2P와 같은 숨김 서비스 네트워크에 노출하는 것은 더욱 위험해집니다. 이러한 서비스를 노출하려면 비밀번호 같은 것으로 보호해야 하며, I2P의 경우 훨씬 더 철저하고 안전한 선택지는 암호화된 LeaseSet(I2P 목적지 접속 정보)일 수 있습니다.

**계속하기 전에, 다음 절차를 Encrypted LeaseSet 없이 수행하면 I2P router의 보안이 무력화된다는 점을 반드시 숙지하십시오. Encrypted LeaseSet 없이 I2P를 통해 router 콘솔 접근을 구성하지 마십시오. 또한, 여러분이 제어하지 않는 어떤 기기와도 Encrypted LeaseSet PSK를 공유하지 마십시오.**

I2P를 통해 공유하면 유용하지만 오직 Encrypted LeaseSet과 함께해야 하는 서비스 중 하나가 바로 I2P router 콘솔 자체입니다. 한 머신에서 I2P router 콘솔을 Encrypted LeaseSet으로 I2P에 노출하면, 브라우저가 있는 다른 머신에서 원격 I2P 인스턴스를 관리할 수 있습니다. 저는 이를 평소 운영하는 I2P 서비스들을 원격으로 모니터링하는 데 유용하게 사용합니다. 또한 장기간 토렌트를 시드하는 서버를 모니터링하고 I2PSnark에 접근하는 방법으로도 사용할 수 있습니다.

설명하는 데 시간이 걸리더라도, Encrypted LeaseSet 설정은 Hidden Services Manager UI를 통해 간단히 구성할 수 있습니다.

## "서버"에서

먼저 http://127.0.0.1:7657/i2ptunnelmgr 에서 Hidden Services Manager를 열고, "I2P Hidden Services."라고 표시된 섹션의 맨 아래로 스크롤하십시오. 호스트 "127.0.0.1"과 포트 "7657"로 새로운 숨겨진 서비스를 생성하고, 이러한 "Tunnel Cryptography Options"을 사용하여 숨겨진 서비스를 저장하십시오.

그런 다음 Hidden Services Manager 메인 페이지에서 새 tunnel을 선택하십시오. 이제 Tunnel Cryptography Options에 첫 번째 Pre-Shared Key(사전 공유 키)가 포함되어 있어야 합니다. 다음 단계를 위해 tunnel의 Encrypted Base32 Address와 함께 이를 복사해 두십시오.

## "클라이언트"에서

이제 은닉 서비스에 연결할 클라이언트 컴퓨터로 전환한 다음, 이전에 받은 키를 추가하기 위해 http://127.0.0.1:7657/configkeyring 의 Keyring Configuration 페이지를 방문하세요. 먼저 서버의 Base32를 "Full destination, name, Base32, or hash."로 라벨된 필드에 붙여넣습니다. 다음으로 서버의 Pre-Shared Key를 "Encryption Key" 필드에 붙여넣습니다. 저장을 클릭하면 Encrypted LeaseSet을 사용하여 은닉 서비스에 안전하게 방문할 준비가 완료되었습니다.

## 이제 I2P를 원격으로 관리할 준비가 되었습니다

보시다시피, I2P는 Hidden Service 관리자에게 전 세계 어디에서나 자신의 I2P 연결을 안전하게 관리할 수 있게 해 주는 고유한 기능을 제공합니다. 같은 이유로 동일한 기기에 보관 중인 다른 Encrypted LeaseSets는 SSH 서버, 내 서비스 컨테이너를 관리하는 데 사용하는 Portainer 인스턴스, 그리고 내 개인 NextCloud 인스턴스를 가리킵니다. I2P를 사용하면 진정으로 사적이고 항상 접근 가능한 셀프 호스팅이 실현 가능한 목표가 되며, 사실 Encrypted LeaseSets 덕분에 이것은 우리가 특히 잘할 수 있는 일 중 하나라고 생각합니다. 이를 통해 I2P는 자체 호스팅된 홈 자동화를 보호하는 열쇠가 되거나, 더 프라이빗한 새로운 피어 투 피어 웹의 중추가 될 수도 있습니다.
