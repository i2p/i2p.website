---
title: "SAM V3"
description: "비자바 I2P 애플리케이션을 위한 Simple Anonymous Messaging 프로토콜"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM은 I2P와 상호작용하기 위한 간단한 클라이언트 프로토콜입니다. SAM은 비Java 애플리케이션이 I2P 네트워크에 연결하기 위한 권장 프로토콜이며, 여러 router 구현에서 지원됩니다. Java 애플리케이션은 streaming 또는 I2CP API를 직접 사용해야 합니다.

SAMv3 버전은 I2P 릴리스 0.7.3(2009년 5월)에 도입되었으며 안정적이고 지원되는 인터페이스입니다. 3.1도 안정적이며 서명 타입 옵션을 지원하므로 강력히 권장됩니다. 더 최신의 3.x 버전들은 고급 기능을 지원합니다. i2pd는 현재 대부분의 3.2 및 3.3 기능을 지원하지 않는다는 점에 유의하세요.

대안: [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (더 이상 사용되지 않음)](/docs/api/bob). 더 이상 사용되지 않는 버전: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## 알려진 SAM 라이브러리

경고: 이 중 일부는 매우 오래되었거나 지원되지 않을 수 있습니다. 아래에 명시된 경우를 제외하고는 I2P 프로젝트에서 테스트하거나 검토하거나 유지 관리하지 않습니다. 직접 조사해 보시기 바랍니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## 빠른 시작

기본적인 TCP 전용 피어투피어 애플리케이션을 구현하려면, 클라이언트는 다음 명령어들을 지원해야 합니다:

- `HELLO VERSION MIN=3.1 MAX=3.1` - 나머지 모든 명령에 필요함
- `DEST GENERATE SIGNATURE_TYPE=7` - 개인 키와 destination 생성을 위해
- `NAMING LOOKUP NAME=...` - .i2p 주소를 destination으로 변환하기 위해
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=4,0` - STREAM CONNECT와 STREAM ACCEPT에 필요
- `STREAM CONNECT ID=... DESTINATION=...` - 나가는 연결을 만들기 위해
- `STREAM ACCEPT ID=...` - 들어오는 연결을 수락하기 위해

## 개발자를 위한 일반 지침

### 애플리케이션 설계

SAM 세션(또는 I2P 내부에서는 tunnel pool이나 터널 집합)은 장기간 유지되도록 설계되었습니다. 대부분의 애플리케이션은 시작 시 생성되고 종료 시 닫히는 하나의 세션만 필요합니다. I2P는 회로가 빠르게 생성되고 폐기될 수 있는 Tor와 다릅니다. 둘 이상의 동시 세션을 사용하거나 빠르게 생성하고 폐기하는 애플리케이션을 설계하기 전에 신중히 고려하고 I2P 개발자들과 상의하세요. 대부분의 위협 모델은 모든 연결에 고유한 세션을 요구하지 않습니다.

또한, 애플리케이션 설정(그리고 router 설정에 대한 사용자 안내, 또는 router를 번들로 제공하는 경우 router 기본값)이 사용자들이 소비하는 것보다 더 많은 자원을 네트워크에 기여하도록 보장해 주시기 바랍니다. I2P는 peer-to-peer 네트워크이며, 인기 있는 애플리케이션이 네트워크를 영구적인 혼잡 상태로 몰아간다면 네트워크가 생존할 수 없습니다.

### 호환성 및 테스트

Java I2P와 i2pd router 구현체는 독립적이며 동작, 기능 지원, 기본값에서 미세한 차이가 있습니다. 두 router의 최신 버전으로 애플리케이션을 테스트해 주세요.

i2pd SAM은 기본적으로 활성화되어 있지만 Java I2P SAM은 그렇지 않습니다. 사용자에게 Java I2P에서 SAM을 활성화하는 방법(router 콘솔의 /configclients를 통해)에 대한 지침을 제공하거나, 초기 연결이 실패할 경우 "I2P가 실행 중이고 SAM 인터페이스가 활성화되어 있는지 확인하세요"와 같은 적절한 오류 메시지를 사용자에게 제공하세요.

Java I2P와 i2pd router는 tunnel 수량에 대해 서로 다른 기본값을 가집니다. Java의 기본값은 2이고 i2pd의 기본값은 5입니다. 대부분의 저~중간 대역폭과 저~중간 연결 수준에서는 2 또는 3으로 충분합니다. Java I2P와 i2pd router에서 일관된 성능을 얻으려면 SESSION CREATE 메시지에서 tunnel 수량을 명시하십시오. 아래를 참조하세요.

애플리케이션이 필요한 리소스만 사용하도록 보장하는 개발자 가이드는 [애플리케이션에 I2P 번들링 가이드](/docs/applications/embedding)를 참조하세요.

### 서명 및 암호화 유형

I2P는 여러 서명 및 암호화 유형을 지원합니다. 하위 호환성을 위해 SAM은 기본적으로 오래되고 비효율적인 유형을 사용하므로, 모든 클라이언트는 더 새로운 유형을 지정해야 합니다.

서명 유형은 DEST GENERATE 및 SESSION CREATE (일시적인 경우) 명령에서 지정됩니다. 모든 클라이언트는 `SIGNATURE_TYPE=7` (Ed25519)로 설정해야 합니다.

암호화 유형은 SESSION CREATE 명령에서 지정됩니다. 여러 암호화 유형이 허용됩니다. 클라이언트는 `i2cp.leaseSetEncType=4` (ECIES-X25519 전용) 또는 `i2cp.leaseSetEncType=4,0` (호환성이 필요한 경우 ECIES-X25519 및 ElGamal)을 설정해야 합니다.

## 버전 3 변경사항

### 버전 3.0 변경사항

버전 3.0은 I2P 릴리스 0.7.3에서 도입되었습니다. SAM v2는 동일한 I2P destination에서 여러 소켓을 *병렬로* 관리할 수 있는 방법을 제공했습니다. 즉, 클라이언트는 한 소켓에서 데이터가 성공적으로 전송되기를 기다릴 필요 없이 다른 소켓에서 데이터를 전송할 수 있었습니다. 하지만 모든 데이터가 동일한 클라이언트-to-SAM 소켓을 통해 전송되어 클라이언트가 관리하기 상당히 복잡했습니다.

SAM v3는 소켓을 다른 방식으로 관리합니다: 각 *I2P socket*은 고유한 클라이언트-SAM 소켓과 일치하며, 이는 처리하기 훨씬 간단합니다. 이는 [BOB](/docs/api/bob)와 유사합니다.

SAM v3는 또한 I2P를 통해 데이터그램을 전송하기 위한 UDP 포트를 제공하며, I2P 데이터그램을 클라이언트의 데이터그램 서버로 다시 전달할 수 있습니다.

### 버전 3.1 변경 사항

버전 3.1은 Java I2P 릴리스 0.9.14(2014년 7월)에서 도입되었습니다. SAM 3.1은 SAM 3.0보다 향상된 서명 유형을 지원하기 때문에 권장되는 최소 SAM 구현입니다. i2pd 또한 대부분의 3.1 기능을 지원합니다.

- DEST GENERATE와 SESSION CREATE가 이제 SIGNATURE_TYPE 매개변수를 지원합니다.
- HELLO VERSION의 MIN과 MAX 매개변수가 이제 선택사항입니다.
- HELLO VERSION의 MIN과 MAX 매개변수가 이제 "3"과 같은 단일 자릿수 버전을 지원합니다.
- RAW SEND가 이제 브리지 소켓에서 지원됩니다.

### 버전 3.2 변경사항

버전 3.2는 Java I2P 릴리스 0.9.24(2016년 1월)에서 도입되었습니다. i2pd는 현재 대부분의 3.2 기능을 지원하지 않는다는 점에 유의하십시오.

#### I2CP 포트 및 프로토콜 지원

- SESSION CREATE 옵션 FROM_PORT와 TO_PORT
- SESSION CREATE STYLE=RAW 옵션 PROTOCOL
- STREAM CONNECT, DATAGRAM SEND, RAW SEND 옵션 FROM_PORT와 TO_PORT
- RAW SEND 옵션 PROTOCOL
- DATAGRAM RECEIVED, RAW RECEIVED, 그리고 전달되거나 수신된 스트림 및 응답 가능한 datagram에 FROM_PORT와 TO_PORT 포함
- RAW 세션 옵션 HEADER=true는 전달된 raw datagram 앞에 PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn을 포함하는 줄이 추가되도록 함
- 포트 7655를 통해 전송되는 datagram의 첫 번째 줄은 이제 임의의 3.x 버전으로 시작할 수 있음
- 포트 7655를 통해 전송되는 datagram의 첫 번째 줄은 FROM_PORT, TO_PORT, PROTOCOL 옵션 중 임의의 것을 포함할 수 있음
- RAW RECEIVED에 PROTOCOL=nnn 포함

#### SSL 및 인증

- 인증을 위한 HELLO 매개변수의 USER/PASSWORD. [아래](#authorization)를 참조하세요.
- AUTH 명령을 통한 선택적 인증 구성. [아래](#authorization-configuration-sam-32-or-higher-optional-feature)를 참조하세요.
- 제어 소켓에서 선택적 SSL/TLS 지원. [아래](#ssl)를 참조하세요.
- STREAM FORWARD 옵션 SSL=true

#### 멀티스레딩

- 동일한 세션 ID에서 동시 대기 중인 STREAM ACCEPT가 허용됩니다.

#### 명령행 파싱 및 연결 유지

- 세션과 소켓을 닫기 위한 선택적 명령어 QUIT, STOP, EXIT. [아래](#quitstopexitinvisible-sam-32-or-higher-optional-features)를 참조하세요.
- 명령어 파싱이 UTF-8을 적절히 처리합니다
- 명령어 파싱이 따옴표 내부의 공백을 안정적으로 처리합니다
- 백슬래시 '\\'로 명령줄에서 따옴표를 이스케이프할 수 있습니다
- telnet을 통한 테스트의 편의를 위해 서버에서 명령어를 대문자로 매핑하는 것을 권장합니다.
- PROTOCOL 또는 PROTOCOL=과 같은 빈 옵션 값이 허용될 수 있으며, 구현에 따라 다릅니다.
- keepalive를 위한 PING/PONG. 아래를 참조하세요.
- 서버는 HELLO 또는 후속 명령어에 대한 타임아웃을 구현할 수 있으며, 구현에 따라 다릅니다.

### 버전 3.3 변경사항

버전 3.3은 Java I2P 릴리스 0.9.25(2016년 3월)에서 도입되었습니다. i2pd는 현재 대부분의 3.3 기능을 지원하지 않는다는 점에 유의하세요.

- 동일한 세션이 스트림, 데이터그램 및 raw를 동시에 사용할 수 있습니다. 들어오는 패킷과 스트림은 I2P 프로토콜과 to-port를 기반으로 라우팅됩니다. [아래 PRIMARY 섹션](#sam-primary-sessions-v33-and-higher)을 참조하세요.
- DATAGRAM SEND 및 RAW SEND는 이제 SEND_TAGS, TAG_THRESHOLD, EXPIRES, SEND_LEASESET 옵션을 지원합니다. [아래 데이터그램 전송 섹션](#sending-repliable-or-raw-datagrams)을 참조하세요.

### 2025-04 변경 사항

2025년 4월 여기에서 두 가지 제안이 승인되어 명세에 반영되었습니다. 지원 여부를 나타내기 위한 버전 변경은 없습니다. 일부 구현체는 아직 이를 지원하지 않으며, 다른 구현체의 경우 지원이 초기 단계입니다.

- Datagram 2/3 지원 (제안 163). SESSION CREATE 및 SESSION ADD(서브세션)에서 지정됨. 아래 참조.
- leaseset 옵션 검색 (제안 167). NAMING LOOKUP OPTIONS=true로 지정됨. 아래 참조.

## 버전 3 프로토콜

### 간단한 익명 메시징(SAM) 버전 3.3 사양 개요

클라이언트 응용 프로그램은 SAM 브리지와 통신하며, SAM 브리지는 모든 I2P 기능을 처리합니다([가상 스트림의 경우 스트리밍 라이브러리](/docs/api/streaming) 사용, 데이터그램의 경우 [I2CP](/docs/protocol/i2cp) 직접 사용).

기본적으로 클라이언트와 SAM 브리지 간의 통신은 암호화되지 않으며 인증되지 않습니다. SAM 브리지는 SSL/TLS 연결을 지원할 수 있으나, 설정 및 구현에 관한 자세한 내용은 이 사양의 범위를 벗어납니다. SAM 3.2부터 초기 핸드셰이크 시 선택적인 인증 사용자 이름/비밀번호 매개변수가 지원되며, 브리지에서 이를 요구할 수 있습니다.

I2P 통신은 여러 가지 형태를 가질 수 있습니다:

- [가상 스트림](/docs/api/streaming)
- [응답 가능하고 인증된 데이터그램](/docs/specs/datagrams#repliable) (FROM 필드가 있는 메시지)
- [익명 데이터그램](/docs/specs/datagrams#raw) (순수한 익명 메시지)
- [Datagram2](/docs/specs/datagrams#datagram2) (새로운 응답 가능하고 인증된 형식)
- [Datagram3](/docs/specs/datagrams#datagram3) (새로운 응답 가능하지만 비인증 형식)

I2P 통신은 I2P 세션에 의해 지원되며, 각 I2P 세션은 주소(목적지라고 함)에 연결되어 있습니다. I2P 세션은 위의 세 가지 유형 중 하나와 연결되며, [기본 세션](#sam-primary-sessions-v33-and-higher)을 사용하지 않는 한 다른 유형의 통신을 처리할 수 없습니다.

### 인코딩 및 이스케이프

이 모든 SAM 메시지는 개행 문자(\\n)로 끝나는 단일 줄에 전송된다. SAM 3.2 이전에는 7비트 ASCII만 지원되었다. SAM 3.2부터 인코딩은 UTF-8이어야 한다. 모든 UTF-8로 인코딩된 키와 값이 정상적으로 동작해야 한다.

아래 명세에 표시된 형식은 단지 가독성을 위한 것이며, 각 메시지의 첫 두 단어는 특정 순서를 유지해야 하지만 key=value 쌍들의 순서는 변경될 수 있습니다(예: "ONE TWO A=B C=D"나 "ONE TWO C=D A=B" 모두 유효한 표현입니다). 또한 이 프로토콜은 대소문자를 구분합니다. 다음 예시에서 클라이언트가 SAM 브리지로 전송하는 메시지는 "->"로, SAM 브리지가 클라이언트로 전송하는 메시지는 "<-"로 표시합니다.

기본 명령문 또는 응답 라인은 다음 형식 중 하나를 가집니다:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
SAM 3.2에서만 일부 새로운 명령어에 대해 서브명령어 없이 명령어(COMMAND)를 사용하는 것이 지원됩니다.

키=값 쌍은 반드시 단일 공백으로 구분되어야 합니다. (SAM 3.2부터는 여러 개의 공백 사용이 허용됨) 값에 공백이 포함된 경우 반드시 큰따옴표로 둘러싸야 합니다. 예: key="긴 값 텍스트". (SAM 3.2 이전에는 일부 구현에서 이 방식이 신뢰성 있게 작동하지 않을 수 있음)

SAM 3.2 이전에는 이스케이프 메커니즘이 존재하지 않았습니다. SAM 3.2부터는 큰따옴표를 백슬래시 '\'로 이스케이프할 수 있으며, 백슬래시 자체는 두 개의 백슬래시 '\\\\'로 표현할 수 있습니다.

### 빈 값

SAM 3.2 기준으로, KEY, KEY=, 또는 KEY=""와 같은 빈 옵션 값이 구현 방식에 따라 허용될 수 있습니다.

### 대소문자 구분

지정된 프로토콜은 대소문자를 구분합니다. 테스트를 위해 telnet을 사용할 때의 편의를 고려하여, 서버가 명령어를 대문자로 매핑하도록 권장하지만 필수 사항은 아닙니다. 예를 들어 "hello version"과 같은 입력이 작동할 수 있도록 해줍니다. 이는 구현 방식에 따라 달라질 수 있습니다. [I2CP](/docs/protocol/i2cp) 옵션이 손상될 수 있으므로 키나 값을 대문자로 매핑해서는 안 됩니다.

### SAM 연결 핸드셰이크

클라이언트와 브리지가 프로토콜 버전에 합의하기 전까지는 SAM 통신이 이루어질 수 없으며, 이 과정은 클라이언트가 HELLO을 전송하고 브리지가 HELLO REPLY를 응답하는 방식으로 수행됩니다:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
그리고

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
버전 3.1(I2P 0.9.14)부터 MIN 및 MAX 매개변수는 선택 사항입니다. SAM은 주어진 MIN 및 MAX 제약 조건 내에서 가능한 가장 높은 버전을 항상 반환하며, 제약 조건이 없을 경우 현재 서버 버전을 반환합니다.

SAM 브리지가 적절한 버전을 찾을 수 없는 경우, 다음과 같이 응답합니다:

```
<- HELLO REPLY RESULT=NOVERSION
```
요청 형식이 잘못되는 등의 오류가 발생하면 다음과 같이 응답합니다:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

서버의 제어 소켓은 서버와 클라이언트의 설정에 따라 선택적으로 SSL/TLS 지원을 제공할 수 있습니다. 구현체는 다른 전송 계층을 추가로 제공할 수도 있으나, 이는 프로토콜 정의의 범위를 벗어납니다.

#### 인증

인증을 위해 클라이언트는 USER="xxx" PASSWORD="yyy"를 HELLO 파라미터에 추가합니다. 사용자 이름과 비밀번호에는 큰따옴표를 사용하는 것이 권장되지만 필수 사항은 아닙니다. 사용자 이름이나 비밀번호 내부의 큰따옴표는 백슬래시로 이스케이프되어야 합니다. 인증에 실패할 경우 서버는 I2P_ERROR와 메시지를 응답으로 보냅니다. 인증이 필요한 SAM 서버에서는 SSL을 활성화하는 것이 권장됩니다.

#### 타임아웃

서버는 HELLO 또는 후속 명령어에 대해 구현 방식에 따라 타임아웃을 적용할 수 있습니다. 클라이언트는 연결 후 즉시 HELLO와 다음 명령어를 전송해야 합니다.

HELLO를 받기 전에 시간 초과가 발생하면 브리지는 다음으로 응답합니다:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
그리고 연결을 끊습니다.

HELLO를 수신한 후 다음 명령을 받기 전에 타임아웃이 발생하면 브리지는 다음과 같이 응답합니다:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
그리고 연결을 끊습니다.

### I2CP 포트 및 프로토콜

SAM 3.2부터 [I2CP](/docs/protocol/i2cp) 포트와 프로토콜이 SAM 클라이언트 전송자에 의해 지정되어 [I2CP](/docs/protocol/i2cp)로 전달될 수 있으며, SAM 브리지는 수신된 [I2CP](/docs/protocol/i2cp) 포트와 프로토콜 정보를 SAM 클라이언트에 전달합니다.

FROM_PORT와 TO_PORT의 경우, 유효한 범위는 0-65535이며, 기본값은 0입니다.

RAW에만 지정할 수 있는 PROTOCOL의 유효 범위는 0-255이며, 기본값은 18입니다.

SESSION 명령의 경우, 지정된 포트와 프로토콜은 해당 세션의 기본값입니다. 개별 스트림이나 데이터그램의 경우, 지정된 포트와 프로토콜이 세션 기본값을 재정의합니다. 수신된 스트림이나 데이터그램의 경우, 표시된 포트와 프로토콜은 [I2CP](/docs/protocol/i2cp)에서 수신된 그대로입니다.

#### 표준 IP와의 중요한 차이점

I2CP 포트는 I2P 소켓과 데이터그램을 위한 것입니다. SAM에 연결하는 로컬 소켓과는 관련이 없습니다.

- 포트 0은 유효하며 특별한 의미를 가집니다.
- 포트 1~1023은 특별하거나 권한이 부여된 것이 아닙니다.
- 서버는 기본적으로 포트 0에서 수신 대기하며, 이는 "모든 포트"를 의미합니다.
- 클라이언트는 기본적으로 포트 0으로 전송하며, 이는 "임의의 포트"를 의미합니다.
- 클라이언트는 기본적으로 포트 0에서 전송하며, 이는 "지정되지 않음"을 의미합니다.
- 서버는 포트 0에서 서비스를 수신 대기하고 다른 고급 포트에서도 추가 서비스를 수신 대기할 수 있습니다. 이 경우 포트 0의 서비스가 기본값이며, 들어오는 소켓 또는 데이터그램 포트가 다른 서비스와 일치하지 않을 때 해당 서비스에 연결됩니다.
- 대부분의 I2P 목적지는 하나의 서비스만 실행 중이므로 기본값을 사용하고 I2CP 포트 설정을 무시해도 됩니다.
- I2CP 포트를 지정하려면 SAM 3.2 또는 3.3이 필요합니다.
- I2CP 포트가 필요하지 않다면 SAM 3.2 또는 3.3이 필요 없으며, 3.1로 충분합니다.
- 프로토콜 0은 유효하며 "임의의 프로토콜"을 의미하지만, 이는 권장되지 않으며 작동하지 않을 가능성이 높습니다.
- I2P 소켓은 내부 연결 ID에 의해 추적됩니다. 따라서 dest:port:dest:port:protocol의 5튜플이 유일할 필요는 없습니다. 예를 들어, 두 목적지 사이에 동일한 포트를 사용하는 여러 소켓이 존재할 수 있습니다. 클라이언트는 아웃바운드 연결을 위해 "사용 가능한 포트"를 선택할 필요가 없습니다.

여러 subsession을 사용하는 SAM 3.3 애플리케이션을 설계하는 경우, 포트와 프로토콜을 효과적으로 사용하는 방법에 대해 신중히 고려하십시오. 자세한 정보는 [I2CP](/docs/protocol/i2cp) 명세서를 참조하십시오.

### SAM 세션

SAM 세션은 클라이언트가 SAM bridge에 소켓을 열고, 핸드셰이크를 수행하고, SESSION CREATE 메시지를 보내서 생성되며, 소켓이 연결 해제되면 세션이 종료됩니다.

등록된 각 I2P Destination은 세션 ID(또는 닉네임)와 고유하게 연결됩니다. PRIMARY 세션의 하위 세션 ID를 포함하여 세션 ID는 SAM 서버에서 전역적으로 고유해야 합니다. 다른 클라이언트와의 ID 충돌을 방지하기 위해서는 클라이언트가 ID를 무작위로 생성하는 것이 모범 사례입니다.

각 세션은 다음과 고유하게 연결됩니다:

- 클라이언트가 세션을 생성하는 소켓
- 해당 ID(또는 별명)

#### 세션 생성 요청

세션 생성 메시지는 이러한 형식 중 하나만 사용할 수 있습니다 (다른 형식으로 수신된 메시지는 오류 메시지로 응답됩니다):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION은 메시지/스트림을 송수신하는 데 사용해야 할 destination을 지정합니다. $privkey는 [Destination](/docs/specs/common-structures#type_Destination) 뒤에 [Private Key](/docs/specs/common-structures#type_PrivateKey), 그 뒤에 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)가 연결되고, 선택적으로 [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature)가 따라오는 것들을 연결한 것의 base 64입니다. 이는 서명 유형에 따라 바이너리로 663바이트 이상, base 64로 884바이트 이상입니다. 바이너리 형식은 Private Key File에 명시되어 있습니다. 아래 Destination Key Generation 섹션에서 [Private Key](/docs/specs/common-structures#type_PrivateKey)에 대한 추가 참고사항을 확인하세요.

서명 개인키가 모두 0인 경우, [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature) 섹션이 따라옵니다. 오프라인 서명은 STREAM 및 RAW 세션에서만 지원됩니다. 오프라인 서명은 DESTINATION=TRANSIENT로 생성할 수 없습니다. 오프라인 서명 섹션의 형식은 다음과 같습니다:

1. 만료 타임스탬프 (4바이트, 빅 엔디언, 에포크 이후 초 단위, 2106년에 롤오버 발생)
2. 일시적 서명 공개 키의 서명 유형 (2바이트, 빅 엔디언)
3. 일시적 서명 공개 키 (일시적 서명 유형에서 지정한 길이)
4. 오프라인 키로 서명한 위 세 필드의 서명 (목적지 서명 유형에서 지정한 길이)
5. 일시적 서명 개인 키 (일시적 서명 유형에서 지정한 길이)

destination이 TRANSIENT로 지정되면, SAM bridge는 새로운 destination을 생성합니다. 버전 3.1(I2P 0.9.14)부터 destination이 TRANSIENT인 경우, 선택적 매개변수 SIGNATURE_TYPE이 지원됩니다. SIGNATURE_TYPE 값은 [Key Certificates](/docs/specs/common-structures#type_Certificate)에서 지원하는 모든 이름(예: ECDSA_SHA256_P256, 대소문자 구분 안함) 또는 숫자(예: 1)가 될 수 있습니다. 기본값은 DSA_SHA1이며, 이는 원하는 것이 아닙니다. 대부분의 애플리케이션의 경우 SIGNATURE_TYPE=7을 지정해 주세요.

$nickname은 클라이언트가 선택하는 것입니다. 공백은 허용되지 않습니다.

주어진 추가 옵션들은 SAM bridge에서 해석되지 않는 경우 I2P 세션 구성에 전달됩니다 (예: outbound.length=0).

Java I2P와 i2pd router는 터널 수량에 대해 서로 다른 기본값을 가지고 있습니다. Java 기본값은 2이고 i2pd 기본값은 5입니다. 대부분의 저-중간 대역폭과 저-중간 연결 수의 경우, 2 또는 3이면 충분합니다. Java I2P와 i2pd router에서 일관된 성능을 얻으려면 SESSION CREATE 메시지에서 터널 수량을 명시하세요. 예를 들어 inbound.quantity=3 outbound.quantity=3와 같은 옵션을 사용하십시오. 이러한 옵션들과 기타 옵션들은 [아래 링크에 문서화되어 있습니다](#tunnel-i2cp-and-streaming-options).

SAM bridge 자체는 I2P를 통해 통신해야 할 router가 이미 구성되어 있어야 합니다 (필요한 경우 override를 제공하는 방법이 있을 수 있습니다. 예: i2cp.tcp.host=localhost 및 i2cp.tcp.port=7654).

#### 세션 생성 응답

session create 메시지를 받은 후, SAM bridge는 다음과 같이 session status 메시지로 응답합니다:

생성이 성공한 경우:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
$privkey는 [Destination](/docs/specs/common-structures#type_Destination) 다음에 [Private Key](/docs/specs/common-structures#type_PrivateKey), 그 다음에 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)를 연결하고, 선택적으로 [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature)를 추가한 것의 base 64 인코딩입니다. 이는 서명 유형에 따라 바이너리로 663바이트 이상, base 64로 884바이트 이상입니다. 바이너리 형식은 Private Key File에 명시되어 있습니다.

SESSION CREATE에 모든 값이 0인 서명 개인키와 [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature) 섹션이 포함되어 있었다면, SESSION STATUS 응답은 동일한 형식으로 동일한 데이터를 포함할 것입니다. 자세한 내용은 위의 SESSION CREATE 섹션을 참조하세요.

닉네임이 이미 세션과 연결되어 있는 경우:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
destination이 이미 사용 중인 경우:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
목적지가 유효한 개인 목적지 키가 아닌 경우:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
다른 오류가 발생한 경우:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
OK가 아닌 경우, MESSAGE는 세션을 생성할 수 없는 이유에 대한 사람이 읽을 수 있는 정보를 포함해야 합니다.

router는 SESSION STATUS로 응답하기 전에 tunnel을 구축한다는 점에 유의하세요. 이 과정은 몇 초가 걸릴 수 있으며, router 시작 시나 심각한 네트워크 혼잡 상황에서는 1분 이상 걸릴 수도 있습니다. 실패할 경우, router는 몇 분 동안 실패 메시지로 응답하지 않을 것입니다. 응답을 기다리는 동안 짧은 타임아웃을 설정하지 마세요. tunnel 구축이 진행 중인 동안 세션을 포기하고 재시도하지 마세요.

SAM 세션은 연결된 소켓과 함께 생성되고 소멸됩니다. 소켓이 닫히면 세션이 종료되고, 해당 세션을 사용하는 모든 통신이 동시에 종료됩니다. 반대로 어떤 이유로든 세션이 종료되면 SAM bridge가 소켓을 닫습니다.

### SAM 가상 스트림

가상 스트림은 신뢰성 있게 순서대로 전송되는 것이 보장되며, 실패 및 성공 알림을 가능한 한 빨리 제공합니다.

Stream은 두 I2P destination 간의 양방향 통신 소켓이지만, 그 열기는 둘 중 하나에 의해 요청되어야 합니다. 이후에 CONNECT 명령은 SAM 클라이언트가 그러한 요청을 위해 사용합니다. FORWARD / ACCEPT 명령은 SAM 클라이언트가 다른 I2P destination에서 오는 요청을 수신하고자 할 때 사용합니다.

### SAM 가상 스트림: 연결

클라이언트는 다음과 같이 연결을 요청합니다:

- SAM 브리지와 새로운 소켓 열기
- 위와 동일한 HELLO 핸드셰이크 전달
- STREAM CONNECT 명령 전송

#### 연결 요청

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
이것은 ID가 $nickname인 로컬 세션에서 지정된 피어로의 새로운 가상 연결을 설정합니다.

대상은 $destination이며, 이는 [Destination](/docs/specs/common-structures#type_Destination)의 base 64이고, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리로 387바이트 이상)입니다.

**참고:** 2014년경(SAM v3.1)부터 Java I2P는 $destination에 대해 호스트명과 b32 주소도 지원해왔지만, 이전에는 문서화되지 않았습니다. 호스트명과 b32 주소는 이제 Java I2P 0.9.48 릴리스부터 공식적으로 지원됩니다. i2pd router는 2.38.0 릴리스(0.9.50)부터 호스트명과 b32 주소를 지원합니다. 두 router 모두에서 "b32" 지원에는 blinded destinations를 위한 확장된 "b33" 주소 지원이 포함됩니다.

#### 연결 응답

SILENT=true가 전달되면, SAM bridge는 소켓에서 다른 메시지를 발행하지 않습니다. 연결이 실패하면 소켓이 닫힙니다. 연결이 성공하면 현재 소켓을 통과하는 모든 남은 데이터가 연결된 I2P destination 피어로부터 그리고 피어로 전달됩니다.

SILENT=false인 경우(기본값), SAM bridge는 소켓을 전달하거나 종료하기 전에 클라이언트에게 마지막 메시지를 보냅니다:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
RESULT 값은 다음 중 하나일 수 있습니다:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
RESULT가 OK이면, 현재 소켓을 통과하는 모든 나머지 데이터가 연결된 I2P 대상 피어로 전달되고 피어로부터 전달됩니다. 연결이 불가능한 경우(타임아웃 등), RESULT는 적절한 오류 값(선택적으로 사람이 읽을 수 있는 MESSAGE와 함께)을 포함하며, SAM bridge가 소켓을 닫습니다.

router 스트림 연결 타임아웃은 내부적으로 약 1분이며, 구현에 따라 달라집니다. 응답을 기다리는 타임아웃을 더 짧게 설정하지 마십시오.

### SAM 가상 스트림: 수락

클라이언트가 들어오는 연결 요청을 기다리는 방법:

- SAM 브리지로 새 소켓 열기
- 위와 동일한 HELLO 핸드세이크 전달
- STREAM ACCEPT 명령 전송

#### 요청 수락

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
이것은 세션 ${nickname}이 I2P 네트워크로부터 하나의 들어오는 연결 요청을 수신 대기하도록 합니다. 세션에 활성 FORWARD가 있는 동안에는 ACCEPT가 허용되지 않습니다.

SAM 3.2부터는 동일한 세션 ID에서 여러 개의 동시 대기 중인 STREAM ACCEPT가 허용됩니다 (동일한 포트에서도 가능). 3.2 이전 버전에서는 동시 accept가 ALREADY_ACCEPTING 오류로 실패했습니다. 참고: Java I2P는 2016년 1월 0.9.24 릴리스부터 SAM 3.1에서도 동시 ACCEPT를 지원합니다. i2pd도 2023년 12월 2.50.0 릴리스부터 SAM 3.1에서 동시 ACCEPT를 지원합니다.

#### Accept 응답

SILENT=true가 전달되면, SAM bridge는 소켓에서 다른 메시지를 발행하지 않습니다. accept가 실패하면 소켓이 닫힙니다. accept가 성공하면 현재 소켓을 통과하는 모든 나머지 데이터가 연결된 I2P destination 피어로부터/에게 전달됩니다. 안정성을 위해, 그리고 들어오는 연결에 대한 destination을 받기 위해 SILENT=false가 권장됩니다.

SILENT=false인 경우, 이는 기본값이며, SAM bridge는 다음과 같이 응답합니다:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
RESULT 값은 다음 중 하나일 수 있습니다:

```
OK
I2P_ERROR
INVALID_ID
```
결과가 OK가 아니면 SAM bridge에 의해 소켓이 즉시 닫힙니다. 결과가 OK이면 SAM bridge는 다른 I2P peer로부터의 들어오는 연결 요청을 기다리기 시작합니다. 요청이 도착하면 SAM bridge는 이를 수락하고:

SILENT=true가 전달된 경우, SAM bridge는 클라이언트 소켓에 다른 메시지를 발행하지 않습니다. 현재 소켓을 통과하는 모든 나머지 데이터는 연결된 I2P destination 피어로부터 그리고 피어로 전달됩니다.

SILENT=false가 전달된 경우(기본값), SAM bridge는 클라이언트에게 요청하는 피어의 base64 공개 destination key와 SAM 3.2에서만 제공되는 추가 정보를 포함한 ASCII 라인을 전송합니다:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
이 '\\n'으로 종료되는 라인 이후, 현재 소켓을 통과하는 모든 남은 데이터는 피어 중 하나가 소켓을 닫을 때까지 연결된 I2P destination 피어로부터 그리고 피어로 전달됩니다.

#### OK 이후의 오류

드문 경우이지만, SAM bridge는 RESULT=OK를 전송한 후에, 연결이 들어와서 클라이언트에 $destination 라인을 보내기 전에 오류가 발생할 수 있습니다. 이러한 오류에는 router 종료, router 재시작, 그리고 세션 종료가 포함될 수 있습니다. 이런 경우에, SILENT=false일 때, SAM bridge는 다음 라인을 보낼 수 있지만 반드시 그럴 필요는 없습니다 (구현에 따라 다름):

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
소켓을 즉시 닫기 전에. 물론 이 줄은 유효한 Base 64 destination으로 디코딩할 수 없습니다.

### SAM 가상 스트림: FORWARD

클라이언트는 일반적인 소켓 서버를 사용하여 I2P에서 오는 연결 요청을 기다릴 수 있습니다. 이를 위해 클라이언트는 다음을 해야 합니다:

- SAM 브리지와 새로운 소켓을 엽니다
- 위와 동일한 HELLO 핸드셰이크를 전달합니다
- 포워드 명령을 보냅니다

#### 전달 요청

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
이것은 세션 ${nickname}이 I2P 네트워크로부터 들어오는 연결 요청을 수신 대기하도록 합니다. 세션에 대기 중인 ACCEPT가 있는 동안에는 FORWARD가 허용되지 않습니다.

#### 응답 전달

SILENT의 기본값은 false입니다. SILENT가 true이든 false이든 관계없이, SAM bridge는 항상 STREAM STATUS 메시지로 응답합니다. 이는 SILENT=true일 때 STREAM ACCEPT와 STREAM CONNECT의 동작과는 다른 방식임에 주의하세요. STREAM STATUS 메시지는 다음과 같습니다:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
RESULT 값은 다음 중 하나일 수 있습니다:

```
OK
I2P_ERROR
INVALID_ID
```
$host는 SAM이 연결 요청을 전달할 소켓 서버의 호스트명 또는 IP 주소입니다. 지정되지 않으면 SAM은 forward 명령을 실행한 소켓의 IP를 사용합니다.

$port는 SAM이 연결 요청을 전달할 소켓 서버의 포트 번호입니다. 필수 항목입니다.

I2P에서 연결 요청이 도착하면, SAM bridge가 $host:$port로 소켓 연결을 엽니다. 3초 이내에 연결이 수락되면, SAM이 I2P로부터의 연결을 수락하고, 그 다음:

SILENT=true가 전달된 경우, 획득된 현재 소켓을 통과하는 모든 데이터는 연결된 I2P destination 피어로부터 그리고 그 피어로 전달됩니다.

SILENT=false가 전달된 경우(기본값), SAM bridge는 획득된 소켓에서 요청하는 피어의 base64 공개 destination 키를 포함하는 ASCII 라인과 SAM 3.2 전용 추가 정보를 전송합니다:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
이 '\\n'으로 종료되는 라인 이후에는, 소켓을 통과하는 모든 나머지 데이터가 연결된 I2P destination 피어로부터 그리고 피어로 전달되며, 이는 어느 한 쪽이 소켓을 닫을 때까지 계속됩니다.

SAMv3.2부터 SSL=true가 지정되면, 포워딩 소켓이 SSL/TLS를 통해 연결됩니다.

"forwarding" 소켓이 닫히는 즉시 I2P router는 들어오는 연결 요청 수신을 중단합니다.

### SAM 데이터그램

SAMv3는 로컬 데이터그램 소켓을 통해 데이터그램을 송수신하는 메커니즘을 제공합니다. 일부 SAMv3 구현체는 SAM 브리지 소켓을 통해 데이터그램을 송수신하는 구버전 v1/v2 방식도 지원합니다. 두 방식 모두 아래에 문서화되어 있습니다.

I2P는 네 가지 유형의 데이터그램을 지원합니다:

- 응답 가능하고 인증된 데이터그램은 발신자의 대상 주소로 시작하며, 발신자의 서명을 포함하여 수신자가 발신자 주소가 위조되지 않았는지 확인하고 데이터그램에 응답할 수 있도록 합니다. 새로운 Datagram2 형식도 응답 가능하고 인증됩니다.
- 새로운 Datagram3 형식은 응답은 가능하지만 인증되지 않습니다. 발신자 정보는 검증되지 않습니다.
- Raw 데이터그램은 발신자의 대상 주소나 서명을 포함하지 않습니다.

기본 I2CP 포트는 응답 가능한 데이터그램과 raw 데이터그램 모두에 대해 정의됩니다. raw 데이터그램의 경우 I2CP 포트를 변경할 수 있습니다.

일반적인 프로토콜 설계 패턴은 응답 가능한 데이터그램을 식별자와 함께 서버에 전송하고, 서버가 해당 식별자를 포함한 원시 데이터그램으로 응답하여 응답을 요청과 연관시킬 수 있도록 하는 것입니다. 이 설계 패턴은 응답에서 응답 가능한 데이터그램의 상당한 오버헤드를 제거합니다. I2CP 프로토콜 및 포트의 모든 선택은 애플리케이션별로 다르며, 설계자들은 이러한 문제들을 고려해야 합니다.

아래 섹션의 데이터그램 MTU에 대한 중요한 참고사항도 확인하세요.

#### 응답 가능하거나 원시 데이터그램 전송

I2P는 본질적으로 FROM 주소를 포함하지 않지만, 사용 편의성을 위해 추가 레이어가 응답 가능한 데이터그램으로 제공됩니다 - 이는 FROM 주소를 포함하는 최대 31744바이트의 순서 없고 신뢰할 수 없는 메시지입니다 (헤더 자료를 위해 최대 1KB를 남겨둠). 이 FROM 주소는 SAM에 의해 내부적으로 인증되며 (소스를 검증하기 위해 destination의 서명 키를 사용), 재생 공격 방지 기능을 포함합니다.

최소 크기는 1입니다. 최적의 전송 안정성을 위해 권장되는 최대 크기는 약 11KB입니다. 안정성은 메시지 크기에 반비례하며, 지수적으로 감소할 수도 있습니다.

STYLE=DATAGRAM 또는 STYLE=RAW로 SAM 세션을 설정한 후, 클라이언트는 SAM의 UDP 포트(기본값 7655)를 통해 응답 가능한 또는 원시 데이터그램을 전송할 수 있습니다.

이 포트를 통해 전송되는 데이터그램의 첫 번째 줄은 다음 형식을 따라야 합니다. 이는 모두 한 줄로 작성되며(공백으로 구분), 명확성을 위해 여러 줄로 표시됩니다:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0은 SAM의 버전입니다. SAM 3.2부터는 3.x 계열의 모든 버전이 허용됩니다.
- $nickname은 사용될 DATAGRAM 세션의 ID입니다.
- 대상은 $destination이며, 이는 [Destination](/docs/specs/common-structures#type_Destination)의 base64 인코딩된 값으로, 서명 유형에 따라 516자 이상의 base64 문자(이진 형태로 387바이트 이상)를 가집니다. **참고:** 약 2014년경(SAM v3.1부터) Java I2P는 $destination에 대해 호스트명과 b32 주소도 지원해 왔으나, 이전까지는 문서화되지 않았습니다. 호스트명 및 b32 주소는 Java I2P 릴리스 0.9.48부터 공식적으로 지원됩니다. i2pd 라우터는 현재 호스트명과 b32 주소를 지원하지 않으며, 향후 릴리스에서 지원이 추가될 수 있습니다.
- 모든 옵션은 SESSION CREATE에서 지정한 기본값을 재정의하는 데이터그램별 설정입니다.
- SEND_TAGS, TAG_THRESHOLD, EXPIRES, SEND_LEASESET 등 3.3 버전의 옵션은 지원되는 경우 [I2CP](/docs/protocol/i2cp)로 전달됩니다. 자세한 내용은 [I2CP 사양](/docs/protocol/i2cp#msg_SendMessageExpire)을 참조하세요. SAM 서버의 이러한 옵션 지원은 선택적이며, 미지원 시 해당 옵션은 무시됩니다.
- 이 줄은 '\\n'으로 종료됩니다.

첫 번째 줄은 메시지의 나머지 데이터를 지정된 목적지로 보내기 전에 SAM에 의해 삭제됩니다.

응답 가능하고 원시 데이터그램을 전송하는 대체 방법에 대해서는 [DATAGRAM SEND and RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling)를 참조하세요.

#### SAM 응답 가능한 데이터그램: 데이터그램 수신하기

수신된 데이터그램은 SESSION CREATE 명령에서 포워딩 PORT가 지정되지 않은 경우, 데이터그램 세션이 열린 소켓에 SAMv3에 의해 작성됩니다. 이는 데이터그램을 수신하는 v1/v2 호환 방식입니다.

데이터그램이 도착하면, 브리지는 다음 메시지를 통해 클라이언트에게 전달합니다:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
소스는 $destination이며, 이는 [Destination](/docs/specs/common-structures#type_Destination)의 base 64이고, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리로는 387바이트 이상)입니다.

SAM bridge는 클라이언트에게 인증 헤더나 기타 필드를 노출하지 않으며, 오직 발신자가 제공한 데이터만을 전달합니다. 이는 세션이 종료될 때까지(클라이언트가 연결을 끊을 때까지) 계속됩니다.

#### Raw 또는 응답 가능한 데이터그램 전달

datagram 세션을 생성할 때, 클라이언트는 들어오는 메시지를 지정된 ip:port로 전달하도록 SAM에 요청할 수 있습니다. 이는 PORT와 HOST 옵션과 함께 CREATE 명령을 발행하여 수행됩니다:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
$privkey는 [Destination](/docs/specs/common-structures#type_Destination) 다음에 [Private Key](/docs/specs/common-structures#type_PrivateKey), 그 다음에 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)를 연결하고, 선택적으로 [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature)를 추가한 것을 base 64로 인코딩한 것입니다. 이는 서명 유형에 따라 884자 이상의 base 64 문자(바이너리로는 663바이트 이상)가 됩니다. 바이너리 형식은 Private Key File에 명시되어 있습니다.

오프라인 서명은 RAW, DATAGRAM2, DATAGRAM3 데이터그램에서 지원되지만 DATAGRAM에서는 지원되지 않습니다. 자세한 내용은 위의 SESSION CREATE 섹션과 아래의 DATAGRAM2/3 섹션을 참조하세요.

$host는 SAM이 데이터그램을 전달할 데이터그램 서버의 호스트명 또는 IP 주소입니다. 지정되지 않으면 SAM은 forward 명령을 발행한 소켓의 IP를 사용합니다.

$port는 SAM이 데이터그램을 전달할 데이터그램 서버의 포트 번호입니다. $port가 설정되지 않으면 데이터그램은 전달되지 않고, v1/v2 호환 방식으로 제어 소켓에서 수신됩니다.

주어진 추가 옵션들은 SAM bridge에서 해석되지 않는 경우 I2P 세션 구성에 전달됩니다 (예: outbound.length=0). 이러한 옵션들은 [아래에 문서화되어 있습니다](#tunnel-i2cp-and-streaming-options).

전달된 응답 가능한 datagram은 아래에서 설명하는 Datagram3를 제외하고 항상 base64 destination이 접두사로 붙습니다. 응답 가능한 datagram이 도착하면, 브리지는 지정된 host:port로 다음 데이터를 포함하는 UDP 패킷을 전송합니다:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
전달된 원시 데이터그램은 접두사 없이 지정된 host:port로 그대로 전달됩니다. UDP 패킷에는 다음 데이터가 포함됩니다:

```
$datagram_payload
```
SAM 3.2부터, SESSION CREATE에서 HEADER=true가 지정되면, 전달되는 원시 데이터그램 앞에 다음과 같은 헤더 라인이 추가됩니다:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64 인코딩으로, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리에서 387바이트 이상)입니다.

#### SAM 익명 (Raw) 데이터그램

I2P의 대역폭을 최대한 활용하여, SAM은 클라이언트가 익명 datagram을 송수신할 수 있게 하며, 인증과 응답 정보는 클라이언트 자체에서 처리하도록 합니다. 이러한 datagram은 신뢰할 수 없고 순서가 보장되지 않으며, 최대 32768바이트까지 가능합니다.

최소 크기는 1입니다. 최상의 전송 안정성을 위해 권장하는 최대 크기는 약 11 KB입니다.

STYLE=RAW로 SAM 세션을 설정한 후, 클라이언트는 [응답 가능한 데이터그램 전송](#sending-repliable-or-raw-datagrams)과 정확히 같은 방식으로 SAM bridge를 통해 익명 데이터그램을 전송할 수 있습니다.

익명 데이터그램의 경우에도 두 가지 데이터그램 수신 방법을 모두 사용할 수 있습니다.

수신된 데이터그램은 SESSION CREATE 명령에서 포워딩 PORT가 지정되지 않은 경우, 데이터그램 세션이 열린 소켓에 SAMv3에 의해 작성됩니다. 이는 데이터그램을 수신하는 v1/v2 호환 방식입니다.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
익명 데이터그램이 특정 host:port로 전달되어야 할 때, 브리지는 지정된 host:port에 다음 데이터를 포함하는 메시지를 전송합니다:

```
$datagram_payload
```
SAM 3.2부터, SESSION CREATE에서 HEADER=true가 지정되면, 전달되는 원시 데이터그램 앞에 다음과 같은 헤더 라인이 추가됩니다:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
익명 데이터그램을 전송하는 대체 방법은 [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling)를 참조하세요.

#### Datagram 2/3

Datagram 2/3는 2025년 초에 명세된 새로운 형식입니다. 현재 알려진 구현체는 존재하지 않습니다. 현재 상태는 구현 문서를 확인하세요. 자세한 정보는 [명세서](/docs/specs/datagrams)를 참조하세요.

Datagram 2/3 지원을 나타내기 위해 SAM 버전을 증가시킬 현재 계획은 없습니다. 구현체들이 Datagram 2/3는 지원하지만 SAM v3.3 기능은 지원하지 않기를 원할 수 있기 때문에 이는 문제가 될 수 있습니다. 버전 변경은 미정입니다.

Datagram2와 Datagram3 모두 응답 가능합니다. Datagram2만 인증됩니다.

Datagram2는 SAM 관점에서 응답 가능한 데이터그램과 동일합니다. 둘 다 인증됩니다. I2CP 형식과 서명만 다르지만, 이는 SAM 클라이언트에게는 보이지 않습니다. Datagram2는 또한 오프라인 서명을 지원하므로 오프라인 서명된 목적지에서 사용할 수 있습니다.

Datagram2는 이전 버전과의 호환성이 필요하지 않은 새로운 애플리케이션에서 Repliable 데이터그램을 대체하기 위한 것입니다. Datagram2는 Repliable 데이터그램에는 없는 재전송 공격 보호 기능을 제공합니다. 이전 버전과의 호환성이 필요한 경우, 애플리케이션은 SAM 3.3 PRIMARY 세션에서 동일한 세션에 대해 Datagram2와 Repliable을 모두 지원할 수 있습니다.

Datagram3는 응답 가능하지만 인증되지 않습니다. I2CP 형식의 'from' 필드는 destination이 아닌 해시입니다. SAM 서버에서 클라이언트로 전송되는 $destination은 44바이트 base64 해시가 됩니다. 응답을 위해 이를 전체 destination으로 변환하려면, base64 디코딩하여 32바이트 바이너리로 만든 다음, base32 인코딩하여 52자로 만들고 NAMING LOOKUP을 위해 ".b32.i2p"를 추가합니다. 일반적으로 클라이언트는 반복적인 NAMING LOOKUP을 피하기 위해 자체 캐시를 유지해야 합니다.

애플리케이션 설계자는 인증되지 않은 데이터그램의 보안 영향을 매우 신중하게 고려해야 합니다.

#### V3 데이터그램 MTU 고려사항

I2P 데이터그램은 일반적인 인터넷 MTU인 1500바이트보다 클 수 있습니다. 로컬로 전송되는 데이터그램과 516+ 바이트 base64 destination이 접두사로 붙은 전달 가능한 응답형 데이터그램은 해당 MTU를 초과할 가능성이 높습니다. 그러나 Linux 시스템의 localhost MTU는 일반적으로 훨씬 크며, 예를 들어 65536바이트입니다. Localhost MTU는 OS에 따라 달라집니다. I2P 데이터그램은 절대 65536바이트보다 크지 않습니다. 데이터그램 크기는 애플리케이션 프로토콜에 따라 결정됩니다.

SAM 클라이언트가 SAM 서버와 로컬에 있고 시스템이 더 큰 MTU를 지원한다면, 데이터그램은 로컬에서 단편화되지 않을 것입니다. 하지만 SAM 클라이언트가 원격에 있다면, IPv4 데이터그램은 단편화되고 IPv6 데이터그램은 실패할 것입니다 (IPv6는 UDP 단편화를 지원하지 않음).

클라이언트 라이브러리 및 애플리케이션 개발자들은 이러한 문제들을 인지하고 단편화를 방지하며 패킷 손실을 예방하기 위한 권장사항을 문서화해야 하며, 특히 원격 SAM 클라이언트-서버 연결에서 더욱 주의해야 합니다.

#### DATAGRAM SEND, RAW SEND (V1/V2 호환 데이터그램 처리)

SAMv3에서 데이터그램을 전송하는 권장 방법은 위에서 설명한 대로 포트 7655의 데이터그램 소켓을 사용하는 것입니다. 그러나 응답 가능한 데이터그램은 [SAM V1](/docs/api/sam)과 [SAM V2](/docs/api/samv2)에서 설명한 대로 DATAGRAM SEND 명령을 사용하여 SAM bridge 소켓을 통해 직접 전송할 수 있습니다.

릴리스 0.9.14 (버전 3.1)부터 익명 데이터그램을 [SAM V1](/docs/api/sam) 및 [SAM V2](/docs/api/samv2)에 문서화된 바와 같이 RAW SEND 명령을 사용하여 SAM bridge 소켓을 통해 직접 전송할 수 있습니다.

릴리스 0.9.24 (버전 3.2)부터 DATAGRAM SEND와 RAW SEND는 기본 포트를 재정의하기 위해 FROM_PORT=nnnn 및/또는 TO_PORT=nnnn 매개변수를 포함할 수 있습니다. 릴리스 0.9.24 (버전 3.2)부터 RAW SEND는 기본 프로토콜을 재정의하기 위해 PROTOCOL=nnn 매개변수를 포함할 수 있습니다.

이 명령들은 ID 매개변수를 지원하지 *않습니다*. 데이터그램은 적절한 경우 가장 최근에 생성된 DATAGRAM- 또는 RAW-스타일 세션으로 전송됩니다. ID 매개변수에 대한 지원은 향후 릴리스에서 추가될 수 있습니다.

DATAGRAM2 및 DATAGRAM3 형식은 V1/V2 호환 방식으로 지원되지 *않습니다*.

### SAM 주 세션 (V3.3 이상)

*버전 3.3은 I2P 릴리스 0.9.25에서 도입되었습니다.*

*이 명세의 이전 버전에서는 PRIMARY 세션이 MASTER 세션으로 알려져 있었습니다. `i2pd`와 `I2P+` 모두에서는 여전히 MASTER 세션으로만 알려져 있습니다.*

SAM v3.3은 동일한 기본 세션에서 스트리밍, 데이터그램, raw 하위 세션을 실행하고, 같은 스타일의 여러 하위 세션을 실행하는 기능을 지원합니다. 모든 하위 세션 트래픽은 단일 목적지 또는 터널 세트를 사용합니다. I2P로부터의 트래픽 라우팅은 하위 세션의 포트 및 프로토콜 옵션을 기반으로 합니다.

다중화된 하위 세션을 생성하려면, 먼저 주 세션을 생성한 다음 주 세션에 하위 세션을 추가해야 합니다. 각 하위 세션은 고유한 ID와 고유한 수신 프로토콜 및 포트를 가져야 합니다. 하위 세션은 주 세션에서 제거할 수도 있습니다.

PRIMARY 세션과 하위 세션들의 조합을 통해, SAM 클라이언트는 단일 tunnel 세트에서 여러 애플리케이션을 지원하거나, 다양한 프로토콜을 사용하는 하나의 정교한 애플리케이션을 지원할 수 있습니다. 예를 들어, 비트토런트 클라이언트는 피어 간 연결을 위한 스트리밍 하위 세션과 함께 DHT 통신을 위한 데이터그램 및 raw 하위 세션을 설정할 수 있습니다.

#### PRIMARY 세션 생성

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM bridge는 [표준 SESSION CREATE에 대한 응답](#session-creation-response)에서와 같이 성공 또는 실패로 응답합니다.

PRIMARY 세션에서는 PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL, 또는 HEADER 옵션을 설정하지 마십시오. PRIMARY 세션 ID나 제어 소켓에서는 어떤 데이터도 전송할 수 없습니다. STREAM CONNECT, DATAGRAM SEND 등과 같은 모든 명령은 별도의 소켓에서 하위 세션 ID를 사용해야 합니다.

PRIMARY 세션은 router에 연결하고 tunnel을 구축합니다. SAM bridge가 응답하면 tunnel이 구축되었으며 세션에 하위 세션을 추가할 준비가 완료됩니다. 길이, 수량, 별명과 같은 tunnel 매개변수에 관련된 모든 [I2CP](/docs/protocol/i2cp) 옵션은 primary의 SESSION CREATE에서 제공되어야 합니다.

모든 유틸리티 명령어는 기본 세션에서 지원됩니다.

기본 세션이 닫히면 모든 하위 세션도 함께 닫힙니다.

참고: 릴리스 0.9.47 이전에는 STYLE=MASTER를 사용하세요. STYLE=PRIMARY는 릴리스 0.9.47부터 지원됩니다. MASTER는 여전히 하위 호환성을 위해 지원됩니다.

#### 서브세션 생성

PRIMARY 세션이 생성된 것과 동일한 제어 소켓을 사용하여:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM 브리지는 [표준 SESSION CREATE에 대한 응답](#session-creation-response)에서와 같이 성공 또는 실패로 응답합니다. tunnel들이 이미 기본 SESSION CREATE에서 구축되었으므로, SAM 브리지는 즉시 응답해야 합니다.

SESSION ADD에서 DESTINATION 옵션을 설정하지 마세요. 서브세션은 주 세션에서 지정된 destination을 사용합니다. 모든 서브세션은 제어 소켓, 즉 주 세션을 생성한 동일한 연결에서 추가되어야 합니다.

여러 하위 세션은 들어오는 데이터가 올바르게 라우팅될 수 있도록 충분히 고유한 옵션을 가져야 합니다. 특히, 동일한 스타일의 여러 세션은 서로 다른 LISTEN_PORT 옵션을 가져야 합니다(그리고/또는 RAW의 경우에만 LISTEN_PROTOCOL). 기존 하위 세션과 중복되는 수신 포트 및 프로토콜로 SESSION ADD를 수행하면 오류가 발생합니다.

LISTEN_PORT는 로컬 I2P 포트로, 즉 들어오는 데이터에 대한 수신(TO) 포트입니다. LISTEN_PORT가 지정되지 않으면 FROM_PORT 값이 사용됩니다. LISTEN_PORT와 FROM_PORT가 모두 지정되지 않으면, 들어오는 라우팅은 STYLE과 PROTOCOL만을 기반으로 합니다. LISTEN_PORT와 LISTEN_PROTOCOL에서 0은 모든 값을 의미하며, 즉 와일드카드입니다. LISTEN_PORT와 LISTEN_PROTOCOL이 모두 0이면, 이 서브세션은 다른 서브세션으로 라우팅되지 않는 들어오는 트래픽의 기본값이 됩니다. 들어오는 스트리밍 트래픽(프로토콜 6)은 LISTEN_PROTOCOL이 0이라도 RAW 서브세션으로 라우팅되지 않습니다. RAW 서브세션은 LISTEN_PROTOCOL을 6으로 설정할 수 없습니다. 들어오는 트래픽의 프로토콜과 포트와 일치하는 기본값이나 서브세션이 없으면, 해당 데이터는 삭제됩니다.

데이터 송수신 시에는 기본 세션 ID가 아닌 하위 세션 ID를 사용하세요. STREAM CONNECT, DATAGRAM SEND 등의 모든 명령은 하위 세션 ID를 사용해야 합니다.

모든 유틸리티 명령은 기본 세션이나 서브세션에서 지원됩니다. v1/v2 데이터그램/raw 송수신은 기본 세션이나 서브세션에서 지원되지 않습니다.

#### 서브세션 중지

PRIMARY 세션이 생성된 것과 동일한 제어 소켓을 사용하여:

```
->  SESSION REMOVE
          ID=$nickname
```
이것은 기본 세션에서 하위 세션을 제거합니다. SESSION REMOVE에는 다른 옵션을 설정하지 마세요. 하위 세션은 제어 소켓, 즉 기본 세션을 생성한 동일한 연결에서 제거되어야 합니다. 하위 세션이 제거된 후에는 닫히며 데이터를 보내거나 받는 데 사용할 수 없습니다.

SAM bridge는 [표준 SESSION CREATE에 대한 응답](#session-creation-response)에서와 같이 성공 또는 실패로 응답합니다.

### SAM 유틸리티 명령어

일부 유틸리티 명령어는 기존 세션이 필요하고 일부는 그렇지 않습니다. 자세한 내용은 아래를 참조하세요.

#### 호스트 이름 조회

다음 메시지는 클라이언트가 이름 해결을 위해 SAM bridge에 질의하는 데 사용할 수 있습니다:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
다음과 같이 답변됩니다

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
RESULT 값은 다음 중 하나일 수 있습니다:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
NAME=ME인 경우, 응답에는 현재 세션에서 사용하는 destination이 포함됩니다 (TRANSIENT를 사용하는 경우 유용함). $result가 OK가 아닌 경우, MESSAGE에는 "bad format" 등과 같은 설명 메시지가 포함될 수 있습니다. INVALID_KEY는 요청의 $name에 문제가 있음을 의미하며, 유효하지 않은 문자가 포함되었을 가능성이 있습니다.

$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64 인코딩으로, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리에서 387바이트 이상)입니다.

NAMING LOOKUP은 세션이 먼저 생성될 필요가 없습니다. 하지만 일부 구현에서는 캐시되지 않고 네트워크 쿼리가 필요한 .b32.i2p 조회가 실패할 수 있는데, 이는 조회를 위한 클라이언트 tunnel이 사용할 수 없기 때문입니다.

#### 이름 조회 옵션

NAMING LOOKUP은 router API 0.9.66부터 서비스 조회를 지원하도록 확장되었습니다. 지원 여부는 구현체에 따라 다를 수 있습니다. 추가 정보는 proposal 167을 참조하세요.

NAMING LOOKUP NAME=example.i2p OPTIONS=true는 응답에서 옵션 매핑을 요청합니다. OPTIONS=true일 때 NAME은 전체 base64 destination이 될 수 있습니다.

destination 조회가 성공하고 leaseset에 옵션이 있었다면, 응답에서 destination 다음에 OPTION:key=value 형식의 하나 이상의 옵션이 따라올 것입니다. 각 옵션은 별도의 OPTION: 접두사를 가집니다. leaseset의 모든 옵션이 포함되며, 서비스 레코드 옵션뿐만 아니라 모든 옵션이 포함됩니다. 예를 들어, 향후 정의될 매개변수에 대한 옵션도 있을 수 있습니다. 예시:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

'='를 포함하는 키와 줄바꿈을 포함하는 키 또는 값은 유효하지 않은 것으로 간주되며, 해당 키/값 쌍은 응답에서 제거됩니다. leaseSet에서 옵션을 찾을 수 없거나 leaseSet이 버전 1인 경우, 응답에는 어떤 옵션도 포함되지 않습니다. 조회에서 OPTIONS=true가 설정되었고 leaseSet을 찾을 수 없는 경우, 새로운 결과값 LEASESET_NOT_FOUND가 반환됩니다.

#### Destination 키 생성

다음 메시지를 사용하여 공개 및 개인 base64 키를 생성할 수 있습니다:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
다음과 같이 답변됩니다

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
버전 3.1(I2P 0.9.14) 기준으로 선택적 매개변수 SIGNATURE_TYPE이 지원됩니다. SIGNATURE_TYPE 값은 [키 인증서](/docs/specs/common-structures#type_Certificate)에서 지원하는 임의의 이름(예: ECDSA_SHA256_P256, 대소문자 구분 없음) 또는 숫자(예: 1)일 수 있습니다. 기본값은 DSA_SHA1이며, 이는 원하는 값이 아닙니다. 대부분의 애플리케이션에서는 SIGNATURE_TYPE=7을 지정하시기 바랍니다.

$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64 인코딩으로, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리에서 387바이트 이상)입니다.

$privkey는 [Destination](/docs/specs/common-structures#type_Destination) 다음에 [Private Key](/docs/specs/common-structures#type_PrivateKey), 그 다음에 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)를 연결한 것의 base 64 인코딩으로, 서명 유형에 따라 884개 이상의 base 64 문자(바이너리로는 663바이트 이상)입니다. 바이너리 형식은 Private Key File에 명시되어 있습니다.

256바이트 바이너리 [Private Key](/docs/specs/common-structures#type_PrivateKey)에 대한 참고사항: 이 필드는 버전 0.6(2005년) 이후로 사용되지 않습니다. SAM 구현체는 이 필드에 랜덤 데이터나 모든 0을 보낼 수 있으므로, base 64에서 AAAA 문자열이 나타나더라도 놀라지 마세요. 대부분의 애플리케이션은 단순히 base 64 문자열을 저장하고 SESSION CREATE에서 그대로 반환하거나, 저장을 위해 바이너리로 디코딩한 다음 SESSION CREATE를 위해 다시 인코딩합니다. 하지만 애플리케이션은 base 64를 디코딩하고, PrivateKeyFile 사양에 따라 바이너리를 파싱하고, 256바이트 private key 부분을 버린 다음, SESSION CREATE를 위해 재인코딩할 때 이를 256바이트의 랜덤 데이터나 모든 0으로 교체할 수도 있습니다. PrivateKeyFile 사양의 다른 모든 필드는 반드시 보존되어야 합니다. 이렇게 하면 파일 시스템 저장 공간을 256바이트 절약할 수 있지만 대부분의 애플리케이션에서는 그만한 가치가 없을 것입니다. 추가 정보와 배경에 대해서는 proposal 161을 참조하세요.

DEST GENERATE는 세션이 먼저 생성될 필요가 없습니다.

DEST GENERATE는 오프라인 서명을 사용하는 목적지를 생성하는 데 사용할 수 없습니다.

#### PING/PONG (SAM 3.2 이상)

클라이언트 또는 서버 중 어느 쪽이든 다음을 전송할 수 있습니다:

```
PING[ arbitrary text]
```
제어 포트에서 다음 응답과 함께:

```
PONG[ arbitrary text from the ping]
```
제어 소켓 keepalive에 사용됩니다. 양쪽 모두 합리적인 시간 내에 응답이 수신되지 않으면 세션과 소켓을 닫을 수 있으며, 이는 구현에 따라 달라집니다.

클라이언트로부터 PONG을 기다리는 중 타임아웃이 발생하면, 브리지는 다음을 보낼 수 있습니다:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
그리고 연결을 끊습니다.

브리지로부터 PONG을 기다리는 중에 타임아웃이 발생하면, 클라이언트는 단순히 연결을 끊을 수 있습니다.

PING/PONG은 세션이 먼저 생성되어야 한다는 요구사항이 없습니다.

#### QUIT/STOP/EXIT (SAM 3.2 이상, 선택적 기능)

QUIT, STOP, EXIT 명령어는 세션과 소켓을 닫습니다. 이 구현은 선택사항이며, telnet을 통한 테스트 편의를 위한 것입니다. 소켓이 닫히기 전에 응답이 있는지 여부(예: SESSION STATUS 메시지)는 구현별로 다르며 이 사양의 범위를 벗어납니다.

QUIT/STOP/EXIT는 먼저 세션이 생성되어야 할 필요가 없습니다.

#### HELP (선택적 기능)

서버는 HELP 명령을 구현할 수 있습니다. 구현은 선택사항이며, telnet을 통한 테스트를 용이하게 하기 위한 것입니다. 출력 형식과 출력 종료 감지는 구현에 따라 다르며 이 사양의 범위를 벗어납니다.

HELP는 먼저 세션이 생성될 필요가 없습니다.

#### 인증 구성 (SAMv3.2 이상, 선택 기능)

AUTH 명령을 사용한 인증 구성. SAM 서버는 자격 증명의 지속적인 저장을 용이하게 하기 위해 이러한 명령을 구현할 수 있습니다. 이러한 명령 이외의 인증 구성은 구현별로 다르며 이 사양의 범위를 벗어납니다.

- AUTH ENABLE는 이후 연결에 대한 인증을 활성화합니다
- AUTH DISABLE는 이후 연결에 대한 인증을 비활성화합니다
- AUTH ADD USER="foo" PASSWORD="bar"는 사용자/비밀번호를 추가합니다
- AUTH REMOVE USER="foo"는 해당 사용자를 제거합니다

사용자와 비밀번호에 대해 큰따옴표를 사용하는 것이 권장되지만 필수는 아닙니다. 사용자 또는 비밀번호 내의 큰따옴표는 백슬래시로 이스케이프해야 합니다. 실패 시 서버는 I2P_ERROR와 메시지로 응답합니다.

AUTH는 세션이 먼저 생성되어야 한다는 요구사항이 없습니다.

### RESULT 값

다음은 RESULT 필드가 가질 수 있는 값들과 그 의미입니다:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
다양한 구현체들이 여러 시나리오에서 어떤 RESULT를 반환하는지에 대해 일관성이 없을 수 있습니다.

OK를 제외한 RESULT를 포함하는 대부분의 응답에는 추가 정보가 담긴 MESSAGE도 포함됩니다. MESSAGE는 일반적으로 문제 디버깅에 도움이 됩니다. 그러나 MESSAGE 문자열은 구현에 따라 달라지며, SAM 서버가 현재 로케일로 번역할 수도 있고 번역하지 않을 수도 있으며, 예외와 같은 내부 구현별 정보를 포함할 수 있고, 예고 없이 변경될 수 있습니다. SAM 클라이언트는 MESSAGE 문자열을 사용자에게 노출하도록 선택할 수 있지만, 이러한 문자열을 기반으로 프로그래밍적 결정을 내려서는 안 됩니다. 그렇게 하면 불안정할 수 있기 때문입니다.

### 터널, I2CP 및 스트리밍 옵션

이러한 옵션들은 SAM SESSION CREATE 라인에서 name=value 쌍으로 전달될 수 있습니다.

모든 세션에는 [tunnel 길이와 수량과 같은 I2CP 옵션](/docs/protocol/i2cp#options)이 포함될 수 있습니다. STREAM 세션에는 [Streaming 라이브러리 옵션](/docs/api/streaming#options)이 포함될 수 있습니다.

옵션 이름과 기본값에 대해서는 해당 참고 문서를 확인하세요. 참조된 문서는 Java router 구현에 대한 것입니다. 기본값은 변경될 수 있습니다. 옵션 이름과 값은 대소문자를 구분합니다. 다른 router 구현체들은 모든 옵션을 지원하지 않을 수 있으며 다른 기본값을 가질 수 있습니다. 자세한 내용은 router 문서를 참조하세요.

### BASE 64 참고 사항

Base 64 인코딩은 I2P 표준 Base 64 알파벳 "A-Z, a-z, 0-9, -, ~"을 사용해야 합니다.

### 기본 SAM 설정

기본 SAM 포트는 7656입니다. SAM은 Java I2P Router에서 기본적으로 활성화되지 않으며, router console의 클라이언트 구성 페이지나 clients.config 파일에서 수동으로 시작하거나 자동으로 시작되도록 구성해야 합니다. 기본 SAM UDP 포트는 7655이며, 127.0.0.1에서 수신 대기합니다. 이러한 설정은 Java router에서 호출 시 sam.udp.port=nnnnn 및/또는 sam.udp.host=w.x.y.z 인수를 추가하거나 SESSION 라인에서 변경할 수 있습니다.

다른 router의 구성은 구현에 따라 다릅니다. [여기 i2pd 구성 가이드](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/)를 참조하세요.
