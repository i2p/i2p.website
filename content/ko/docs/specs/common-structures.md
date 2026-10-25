---
title: "공통 구조 명세서"
description: "모든 I2P 프로토콜에 공통되는 데이터 타입"
slug: "common-structures"
category: "설계"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

이 문서는 [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU](/docs/legacy/ssu/) 등과 같은 모든 I2P 프로토콜에 공통으로 사용되는 일부 데이터 타입을 설명합니다.

## 일반 타입 명세

### 정수

#### 설명

음이 아닌 정수를 나타냅니다.

#### 목차

부호 없는 정수를 나타내는 네트워크 바이트 순서(빅 엔디안)의 1~8바이트입니다.

### 날짜

#### 설명

GMT 시간대에서 1970년 1월 1일 자정 이후의 밀리초 수입니다. 숫자가 0이면 날짜가 정의되지 않았거나 null입니다.

#### 목차

8바이트 [Integer](#integer)

### 문자열

#### 설명

UTF-8로 인코딩된 문자열을 나타냅니다.

#### 목차

1바이트 이상으로, 첫 번째 바이트는 문자열의 바이트 수(문자 수가 아님!)이고 나머지 0-255 바이트는 null로 종료되지 않는 UTF-8 인코딩된 문자 배열입니다. 길이 제한은 255바이트(문자 수가 아님)입니다. 길이는 0이 될 수 있습니다.

### PublicKey

#### 설명

이 구조는 ElGamal이나 다른 비대칭 암호화에서 사용되며, 소수가 아닌 지수만을 나타냅니다. 소수는 상수이며 암호화 명세서 [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)에 정의되어 있습니다. 다른 암호화 방식들이 정의되는 과정에 있으며, 아래 표를 참조하세요.

#### 목차

키 유형과 길이는 문맥에서 추론되거나 Destination 또는 RouterInfo의 Key Certificate, 또는 [LeaseSet2](#leaseset2)나 기타 데이터 구조의 필드에서 지정됩니다. 기본 유형은 ElGamal입니다. 릴리스 0.9.38부터 문맥에 따라 다른 유형들이 지원될 수 있습니다. 별도로 명시되지 않는 한 키는 big-endian입니다.

X25519 키는 릴리스 0.9.44부터 Destinations과 LeaseSet2에서 지원됩니다. X25519 키는 릴리스 0.9.48부터 RouterIdentities에서 지원됩니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PublicKey](http://docs.i2p-projekt.de/net/i2p/data/PublicKey.html)

### PrivateKey

#### 설명

이 구조는 ElGamal이나 다른 비대칭 복호화에서 사용되며, 소수가 아닌 지수만을 나타냅니다. 소수는 상수이며 암호화 사양 [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)에서 정의됩니다. 다른 암호화 방식들도 정의 과정에 있으며, 아래 표를 참조하십시오.

#### 목차

키 유형과 길이는 컨텍스트에서 추론되거나 데이터 구조 또는 개인키 파일에 별도로 저장됩니다. 기본 유형은 ElGamal입니다. 0.9.38 릴리스부터 컨텍스트에 따라 다른 유형들이 지원될 수 있습니다. 키는 별도로 명시되지 않는 한 big-endian 방식입니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1632</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2400</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3168</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PrivateKey](http://docs.i2p-projekt.de/net/i2p/data/PrivateKey.html)

### SessionKey

#### 설명

이 구조는 대칭 AES256 암호화 및 복호화에 사용됩니다.

#### 목차

32바이트

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### 설명

이 구조는 서명을 검증하는 데 사용됩니다.

#### 목차

키 유형과 길이는 맥락에서 추론되거나 Destination의 Key Certificate에서 지정됩니다. 기본 유형은 DSA_SHA1입니다. 0.9.12 릴리스부터는 맥락에 따라 다른 유형들이 지원될 수 있습니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### 주의사항

* 키가 두 개의 요소로 구성된 경우(예: 점 X,Y), 필요한 경우 각 요소를 선행 0으로 length/2까지 패딩하여 직렬화됩니다.

* 모든 타입은 Big Endian이며, EdDSA와 RedDSA는 예외로 Little Endian 형식으로 저장되고 전송됩니다.

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### 설명

이 구조체는 서명을 생성하는 데 사용됩니다.

#### 목차

키 유형과 길이는 생성할 때 지정됩니다. 기본 유형은 DSA_SHA1입니다. 0.9.12 릴리스부터는 컨텍스트에 따라 다른 유형들이 지원될 수 있습니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### 참고사항

* 키가 두 개의 요소로 구성된 경우 (예: 점 X,Y), 필요시 각 요소를 앞자리 0으로 채워서 길이/2로 맞춘 후 직렬화합니다.

* EdDSA와 RedDSA를 제외한 모든 유형은 Big Endian이며, EdDSA와 RedDSA는 Little Endian 형식으로 저장되고 전송됩니다.

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### 서명

#### 설명

이 구조는 어떤 데이터의 서명을 나타냅니다.

#### 목차

서명 타입과 길이는 사용된 키의 타입으로부터 추론됩니다. 기본 타입은 DSA_SHA1입니다. 릴리스 0.9.12부터는 컨텍스트에 따라 다른 타입들이 지원될 수 있습니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### 주의사항

* 서명이 두 개의 요소로 구성된 경우 (예: R, S 값), 각 요소를 필요시 앞에 0을 붙여 length/2로 패딩하여 직렬화됩니다.

* EdDSA와 RedDSA를 제외한 모든 타입은 Big Endian 형식이며, EdDSA와 RedDSA는 Little Endian 형식으로 저장되고 전송됩니다.

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### 해시

#### 설명

어떤 데이터의 SHA256을 나타냅니다.

#### 목차

32바이트

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### 세션 태그

참고: ECIES-X25519 목적지(ratchet)와 ECIES-X25519 router에 대한 세션 태그는 8바이트입니다. [ECIES](/docs/specs/ecies/) 및 [ECIES-ROUTERS](/docs/specs/ecies-routers/)를 참조하세요.

#### 설명

무작위 수

#### 목차

32바이트

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### 설명

터널 내 각 router에 고유한 식별자를 정의합니다. Tunnel ID는 일반적으로 0보다 큰 값이며, 특별한 경우를 제외하고는 0 값을 사용하지 마세요.

#### 목차

4바이트 [Integer](#integer)

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### 인증서

#### 설명

인증서는 I2P 네트워크 전반에서 사용되는 다양한 영수증이나 작업 증명을 담는 컨테이너입니다.

#### 목차

인증서 타입을 지정하는 1바이트 [Integer](#integer), 그 다음 인증서 페이로드의 크기를 지정하는 2바이트 [Integer](#integer), 그리고 해당 크기만큼의 바이트들이 이어집니다.

```
+----+----+----+----+----+-/
|type| length  | payload
+----+----+----+----+----+-/

type :: Integer
        length -> 1 byte

length :: Integer
          length -> 2 bytes

payload :: data
           length -> $length bytes
```
#### 참고사항

* [Router Identities](#routeridentity)의 경우, 버전 0.9.15까지는 Certificate가 항상 NULL입니다. 0.9.16부터는 키 유형을 지정하기 위해 Key Certificate가 사용됩니다. 0.9.48부터는 X25519 암호화 공개 키 유형이 허용됩니다. 아래를 참조하십시오.

* [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove)의 경우, Certificate는 항상 NULL이며, 현재 다른 구현은 없습니다.

* [Garlic Messages](/docs/specs/i2np/#msg-garlic)의 경우, Certificate는 항상 NULL이며, 현재 다른 것들은 구현되지 않았습니다.

* [Destinations](#destination)의 경우, Certificate는 NULL이 아닐 수 있습니다. 0.9.12부터 Key Certificate를 사용하여 서명 공개 키 유형을 지정할 수 있습니다. 아래를 참조하세요.

* 구현자들은 Certificate에서 초과 데이터를 금지하도록 주의해야 합니다.
  각 certificate 유형에 대한 적절한 길이가 강제되어야 합니다.

#### 인증서 유형

다음과 같은 인증서 유형이 정의되어 있습니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HashCash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains an ASCII colon-separated hashcash string.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Hidden routers generally do not announce that they are hidden.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40 or 72</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">43 or 75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains a 40-byte DSA signature, optionally followed by the 32-byte Hash of the signing Destination.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains multiple certificates.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 0.9.12. See below for details.</td>
    </tr>
  </tbody>
</table>
#### 키 인증서

키 인증서는 릴리스 0.9.12에서 도입되었습니다. 해당 릴리스 이전에는 모든 PublicKey가 256바이트 ElGamal 키였고, 모든 SigningPublicKey가 128바이트 DSA-SHA1 키였습니다. 키 인증서는 Destination 또는 RouterIdentity에서 PublicKey와 SigningPublicKey의 유형을 나타내고, 표준 길이를 초과하는 모든 키 데이터를 패키징하는 메커니즘을 제공합니다.

certificate 앞에 정확히 384바이트를 유지하고, 초과하는 키 데이터를 certificate 내부에 배치함으로써, Destinations와 Router Identities를 파싱하는 모든 소프트웨어와의 호환성을 유지합니다.

키 인증서 페이로드는 다음을 포함합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Data</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signing Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Signing Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Crypto Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
  </tbody>
</table>
경고: 키 타입 순서는 예상과 반대입니다. Signing Public Key Type이 먼저 옵니다.

정의된 서명 공개키 유형은 다음과 같습니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only; never used for Router Identities</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
정의된 암호화 공개 키 타입은 다음과 같습니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies/">ECIES</a> and proposal 156</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (NONE)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
Key Certificate가 없는 경우, Destination 또는 RouterIdentity의 앞선 384바이트는 256바이트 ElGamal PublicKey와 128바이트 DSA-SHA1 SigningPublicKey로 정의됩니다. Key Certificate가 있는 경우, 앞선 384바이트는 다음과 같이 재정의됩니다:

* 암호화 공개 키의 전체 또는 첫 번째 부분

* 두 키의 총 길이가 384바이트 미만인 경우 랜덤 패딩

* 서명 공개 키의 전체 또는 첫 번째 부분

Crypto Public Key는 시작 부분에 정렬되고 Signing Public Key는 끝 부분에 정렬됩니다. 패딩(있는 경우)은 가운데에 위치합니다. 인증서 내의 초기 키 데이터, 패딩, 그리고 초과 키 데이터 부분의 길이와 경계는 명시적으로 지정되지 않지만, 지정된 키 타입의 길이로부터 도출됩니다. Crypto와 Signing Public Key의 총 길이가 384바이트를 초과하는 경우, 나머지는 Key Certificate에 포함됩니다. Crypto Public Key 길이가 256바이트가 아닌 경우, 두 키 간의 경계를 결정하는 방법은 이 문서의 향후 개정판에서 명시될 예정입니다.

ElGamal 암호화 공개 키와 표시된 서명 공개 키 유형을 사용한 레이아웃 예시:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Padding Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Excess Signing Key Data in Cert</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.Certificate](http://docs.i2p-projekt.de/net/i2p/data/Certificate.html)

#### 노트

* 구현자들은 Key Certificate에서 초과 데이터를 금지하도록 주의해야 합니다.
  각 인증서 유형에 대한 적절한 길이가 강제되어야 합니다.

* 타입 0,0 (ElGamal,DSA_SHA1)의 KEY certificate는 허용되지만 권장되지 않습니다.
  충분히 테스트되지 않았으며 일부 구현에서 문제를 일으킬 수 있습니다.
  (ElGamal,DSA_SHA1) Destination 또는 RouterIdentity의 표준 표현에서는 NULL certificate를 사용하십시오.
  이는 KEY certificate를 사용하는 것보다 4바이트 짧습니다.

### 매핑

#### 설명

키/값 매핑 또는 속성의 집합

#### 목차

2바이트 크기의 Integer 다음에 String=String; 쌍의 연속이 옵니다.

경고: Mapping의 대부분의 사용은 서명된 구조에서 이루어지며, 여기서 Mapping 엔트리들은 키에 따라 정렬되어야 하므로 서명이 불변입니다. 키에 따라 정렬하지 않으면 서명 실패가 발생합니다!

```bytefield
size       | 4 | red    | Integer, 2 bytes
key_string | 4 | blue   | String (len + data)
val_string | 8 | green  | String (len + data)
;          | 8 | yellow | :: A single byte containing ';'
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+
```
</details>
#### 참고사항

* 인코딩이 최적화되지 않았습니다 - '=' 및 ';' 문자 또는 문자열 길이 중 하나가 필요하지만 둘 다 필요하지는 않습니다

#### 설명

* 일부 문서에서는 문자열에 '=' 또는 ';'를 포함할 수 없다고 나와 있지만 이 인코딩은 이를 지원합니다

* 문자열은 UTF-8로 정의되지만 현재 구현에서는 I2CP는 UTF-8을 사용하지만 I2NP는 그렇지 않습니다. 예를 들어, I2NP Database Store Message의 RouterInfo 옵션 매핑에 있는 UTF-8 문자열은 손상됩니다.

* 인코딩은 중복 키를 허용하지만, 매핑이 서명되는 모든 사용에서 중복은 서명 실패를 일으킬 수 있습니다.

* I2NP 메시지에 포함된 매핑들(예: RouterAddress 또는 RouterInfo에서)은
  서명이 불변하도록 키별로 정렬되어야 합니다. 중복 키는
  허용되지 않습니다.

* [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig)에 포함된 매핑은 서명이 불변이 되도록 키별로 정렬되어야 합니다. 중복 키는 허용되지 않습니다.

* 정렬 방법은 문자의 유니코드 값을 사용하여 Java String.compareTo()와 동일하게 정의됩니다.

* 애플리케이션에 따라 다르지만, 키와 값은 일반적으로 대소문자를 구분합니다.

* 키와 값 문자열 길이 제한은 각각 255바이트(문자가 아님)이며, 여기에 길이 바이트가 추가됩니다. 길이 바이트는 0일 수 있습니다.

* 총 길이 제한은 65535바이트이며, 2바이트 크기 필드를 더해 총 65537바이트입니다.

* X25519 암호화 타입과 Ed25519 서명 타입을 가진 Router Identity는 랜덤 데이터의 10개 사본(320바이트)을 포함하며, 압축 시 약 288바이트를 절약할 수 있습니다.

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## 공통 구조 명세서

### KeysAndCert

#### 목차

RouterIdentity 또는 Destination으로 사용되는 암호화 공개 키, 서명 공개 키, 그리고 인증서입니다.

#### 패딩 생성 가이드라인

[PublicKey](#publickey) 뒤에 [SigningPublicKey](#signingpublickey)가 오고, 그 다음에 [Certificate](#certificate)가 따라옵니다.

```bytefield
public_key          | 8 | blue   | PublicKey (partial or full), 256 bytes or as specified in key cert

padding (optional)  | 8 | yellow | random data, pub + pad + sig == 384 bytes

signing_key         | 8 | green  | SigningPublicKey (partial or full), 128 bytes or as specified

certificate         | 3 | purple | Certificate, >= 3 bytes
= total length: 387+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-/

public_key :: `PublicKey` (partial or full)
              length -> 256 bytes or as specified in key certificate

padding :: random data
           length -> 0 bytes or as specified in key certificate
           public_key length + padding length + signing_key length == 384 bytes

signing__key :: `SigningPublicKey` (partial or full)
                length -> 128 bytes or as specified in key certificate

certificate :: `Certificate`
               length -> >= 3 bytes

total length: 387+ bytes
```

</details>
#### 참고사항

이러한 가이드라인은 Proposal 161에서 제안되었고 API 버전 0.9.57에서 구현되었습니다. 이 가이드라인은 0.6 (2005) 이후의 모든 버전과 하위 호환됩니다. 배경과 추가 정보는 Proposal 161을 참조하세요.

ElGamal + DSA-SHA1 이외의 현재 사용되는 키 유형 조합에는 패딩이 존재합니다. 또한 목적지의 경우, 256바이트 공개 키 필드는 버전 0.6(2005년) 이후로 사용되지 않고 있습니다.

구현자는 Destination 공개 키와 Destination 및 Router Identity 패딩을 위한 랜덤 데이터를 생성할 때, 다양한 I2P 프로토콜에서 압축 가능하면서도 여전히 안전하고, Base 64 표현이 손상되거나 안전하지 않은 것으로 보이지 않도록 해야 합니다. 이는 파괴적인 프로토콜 변경 없이 패딩 필드를 제거하는 것의 대부분의 이점을 제공합니다.

엄밀히 말하면, 32바이트 서명 공개키만으로도 (Destination과 Router Identity 모두에서) 그리고 32바이트 암호화 공개키 (Router Identity에서만)는 이러한 구조체들의 SHA-256 해시가 암호학적으로 강력하고 netDb DHT에서 무작위로 분산되는 데 필요한 모든 엔트로피를 제공하는 난수입니다.

그러나 충분한 주의를 기하기 위해 ElG 공개 키 필드와 패딩에 최소 32바이트의 랜덤 데이터를 사용할 것을 권장합니다. 또한 필드가 모두 0이면 Base 64 목적지에 AAAA 문자가 길게 연속되어 나타나 사용자에게 경고나 혼란을 야기할 수 있습니다.

I2NP Database Store Message, Streaming SYN, SSU2 handshake, repliable Datagrams와 같은 I2P 프로토콜에서 전체 KeysAndCert 구조가 높은 압축률을 가질 수 있도록 32바이트의 랜덤 데이터를 필요에 따라 반복합니다.

예시:

* Ed25519 서명 유형을 가진 Destination은
  랜덤 데이터의 11개 복사본(352바이트)을 포함하며, 압축 시 약 320바이트를 절약할 수 있습니다.

* 이것들이 항상 387바이트라고 가정하지 마세요! 이들은 387바이트에 385-386바이트에서 지정된 인증서 길이를 더한 것으로, 0이 아닐 수 있습니다.

구현체들은 당연히 전체 387+ 바이트 구조를 저장해야 합니다. 왜냐하면 구조의 SHA-256 해시가 전체 내용을 포함하기 때문입니다.

#### 설명

* 릴리스 0.9.12부터, 인증서가 Key Certificate인 경우 키 필드의 경계가 달라질 수 있습니다. 자세한 내용은 위의 Key Certificate 섹션을 참조하세요.

* Crypto Public Key는 시작 부분에 정렬되고 Signing Public Key는 끝 부분에 정렬됩니다. 패딩(있는 경우)은 중간에 위치합니다.

* RouterIdentity에 대한 인증서는 0.9.12 릴리스까지 항상 NULL이었습니다.

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### 목차

특정 router를 고유하게 식별하는 방법을 정의합니다

#### 참고사항

KeysAndCert와 동일합니다.

패딩 필드의 랜덤 데이터 생성 가이드라인은 [KeysAndCert](#keysandcert)를 참조하세요.

#### 설명

* 이것들이 항상 387바이트라고 가정하지 마세요! 이들은 387바이트에 385-386바이트에서 지정된 인증서 길이를 더한 것으로, 0이 아닐 수 있습니다.

* 릴리스 0.9.12부터, 인증서가 Key Certificate인 경우 키 필드의 경계가 달라질 수 있습니다. 자세한 내용은 위의 Key Certificate 섹션을 참조하십시오.

* Crypto Public Key는 시작 부분에 정렬되고 Signing Public Key는 끝 부분에 정렬됩니다. 패딩(있는 경우)은 중간에 위치합니다.

* 키 인증서와 ECIES_X25519 공개 키를 가진 RouterIdentity는 릴리스 0.9.48부터 지원됩니다.
  그 이전에는 모든 RouterIdentity가 ElGamal이었습니다.

* 목적지의 공개 키는 버전 0.6(2005년)에서 비활성화된 기존 i2cp-to-i2cp 암호화에 사용되었으며, 현재는 더 이상 사용되지 않는 LeaseSet 암호화의 IV를 제외하고는 사용되지 않습니다. 대신 LeaseSet의 공개 키가 사용됩니다.

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### 목적지

#### 목차

Destination은 메시지가 안전한 전달을 위해 향할 수 있는 특정 엔드포인트를 정의합니다.

#### 주의사항

[KeysAndCert](#keysandcert)와 동일하지만, 공개 키는 사용되지 않으며 유효한 ElGamal 공개 키 대신 무작위 데이터를 포함할 수 있습니다.

공개 키와 패딩 필드를 위한 랜덤 데이터 생성 지침은 [KeysAndCert](#keysandcert)를 참조하세요.

#### 설명

* 이것들이 항상 387바이트라고 가정하지 마세요! 이들은 387바이트에 385-386바이트에 명시된 인증서 길이를 더한 것으로, 이는 0이 아닐 수 있습니다.

* 릴리스 0.9.12부터, 인증서가 Key Certificate인 경우 키 필드의 경계가 달라질 수 있습니다. 자세한 내용은 위의 Key Certificate 섹션을 참조하세요.

* Crypto Public Key는 시작 부분에 정렬되고 Signing Public Key는 끝 부분에 정렬됩니다. 패딩(있는 경우)은 중간에 위치합니다.

* 목적지의 공개 키는 버전 0.6에서 비활성화된 이전 I2CP-to-I2CP 암호화에 사용되었으며, 현재는 사용되지 않습니다.

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### Lease

#### 목차

사용 중단됨. LeaseSet2 및 Lease2를 사용하십시오.

특정 터널이 [대상(Destination)](#destination)을 타겟으로 하는 메시지를 수신할 수 있도록 허가를 정의합니다.

#### 설명

게이트웨이 라우터의 [RouterIdentity](#routeridentity)에 대한 SHA256 [Hash](#hash), 그 다음 [TunnelId](#tunnelid), 마지막으로 종료 [Date](#date).

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | Date, 8 bytes

= Total size 44 bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: `Date`
            length -> 8 bytes
```

</details>
JavaDoc: [net.i2p.data.Lease](http://docs.i2p-projekt.de/net/i2p/data/Lease.html)

### LeaseSet

#### 목차

사용 중단됨. LeaseSet2 및 Lease2를 사용하십시오.

특정 [Destination](#destination)에 대한 현재 승인된 모든 [Leases](#lease)를 포함하며, 마늘 암호화(garlic encryption) 메시지를 암호화하는 데 사용할 수 있는 [PublicKey](#publickey)와 이 구조의 특정 버전을 폐기(revoke)하는 데 사용할 수 있는 [SigningPublicKey](#signingpublickey)를 포함합니다. LeaseSet은 네트워크 데이터베이스(netDb)에 저장되는 두 가지 구조 중 하나이며(다른 하나는 [RouterInfo](#routerinfo)), 포함된 [Destination](#destination)의 SHA256 해시 값으로 키가 지정됩니다.

#### 참고사항

[Destination](#destination), 그 다음에 암호화를 위한 [PublicKey](#publickey), 그리고 이 leaseSet 버전을 철회하는데 사용할 수 있는 [SigningPublicKey](#signingpublickey), 그 다음에 집합에 포함된 [Lease](#lease) 구조의 개수를 지정하는 1바이트 [Integer](#integer), 그 다음에 실제 [Lease](#lease) 구조들, 그리고 마지막으로 [Destination](#destination)의 [SigningPrivateKey](#signingprivatekey)로 서명된 이전 바이트들의 [Signature](#signature).

```bytefield
destination     | 8 | blue   | Destination, >= 387+ bytes
encryption_key  | 8 | green  | PublicKey, 256 bytes
signing_key     | 8 | cyan   | SigningPublicKey, 128 bytes or as specified in destination's key cert
num             | 1 | red    | Integer, 1 byte, number of leases (0-16)
Lease 0         | 7 | yellow | Lease, 44 bytes
Lease 1         | 8 | yellow | Lease, 44 bytes
Lease ($num-1)  | 8 | yellow | Lease, 44 bytes
signature       | 8 | purple | Signature, 40 bytes or as specified in destination's key cert

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

encryption_key :: `PublicKey`
                  length -> 256 bytes

signing_key :: `SigningPublicKey`
               length -> 128 bytes or as specified in destination's key
                         certificate

num :: `Integer`
       length -> 1 byte
       Number of leases to follow
       value: 0 <= num <= 16

leases :: [`Lease`]
          length -> $num*44 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate
```

</details>
#### 설명

* 암호화 키는 종단 간 ElGamal/AES+SessionTag 암호화 [ELGAMAL-AES](/docs/specs/elgamal-aes/)에 사용됩니다. 현재 router 시작 시마다 새로 생성되며, 지속되지 않습니다.

* 서명은 목적지의 서명 공개키를 사용하여 검증할 수 있습니다.

* Lease가 0개인 LeaseSet은 허용되지만 사용되지 않습니다.
  이는 구현되지 않은 LeaseSet 취소를 위해 의도되었습니다.
  모든 LeaseSet2 변형은 최소 하나의 Lease가 필요합니다.

* signing_key는 현재 사용되지 않습니다. LeaseSet 폐기를 위해 의도되었지만 구현되지 않았습니다. 현재 router 시작시마다 새로 생성되며 지속되지 않습니다. signing key 유형은 항상 destination의 signing key 유형과 동일합니다.

* 모든 Lease들 중 가장 빠른 만료 시간이 LeaseSet의 타임스탬프 또는 버전으로 취급됩니다. Router들은 일반적으로 현재 것보다 "더 새로운" LeaseSet이 아니면 저장을 허용하지 않습니다. 가장 오래된 Lease가 이전 LeaseSet의 가장 오래된 Lease와 동일한 새로운 LeaseSet을 게시할 때 주의하세요. 이런 경우 게시하는 router는 일반적으로 가장 오래된 Lease의 만료 시간을 최소 1ms 증가시켜야 합니다.

* 릴리스 0.9.7 이전에는 원본 router가 보낸 DatabaseStore 메시지에 포함될 때, router는 게시된 모든 lease의 만료 시간을 동일한 값(가장 빠른 lease의 만료 시간)으로 설정했습니다. 릴리스 0.9.7부터는 router가 각 lease의 실제 lease 만료 시간을 게시합니다. 이는 구현 세부사항이며 구조 명세의 일부는 아닙니다.

* 총 크기: 40바이트

JavaDoc: [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### 목차

특정 tunnel이 [Destination](#destination)을 대상으로 하는 메시지를 수신할 수 있는 권한을 정의합니다. [Lease](#lease)와 동일하지만 4바이트 end_date를 가집니다. [LeaseSet2](#leaseset2)에서 사용됩니다. 0.9.38부터 지원되며, 자세한 정보는 proposal 123을 참조하세요.

#### 참고사항

게이트웨이 라우터의 [RouterIdentity](#routeridentity)에 대한 SHA256 [Hash](#hash), 그다음 [TunnelId](#tunnelid), 마지막으로 4바이트의 종료 날짜.

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.
```

</details>
#### 설명

* 이 섹션은 오프라인에서 생성될 수 있으며, 또한 생성되어야 합니다.

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### OfflineSignature

#### 목차

이것은 [LeaseSet2Header](#leaseset2header)의 선택적 부분입니다. 스트리밍 및 I2CP에서도 사용됩니다. 0.9.38 버전부터 지원되며, 자세한 내용은 제안서 123을 참조하세요.

#### 참고사항

만료일, sigtype 및 임시 [SigningPublicKey](#signingpublickey), 그리고 [Signature](#signature)를 포함합니다.

```bytefield
expires              | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
sigtype              | 2 | cyan   | 2 byte type of the transient_public_key
_ | 2
transient_public_key | 8 | green  | SigningPublicKey, as inferred from sigtype

signature            | 8 | purple | Signature, as inferred from sigtype of the Destination's key

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4 byte date
           length -> 4 bytes
           Seconds since the epoch, rolls over in 2106.

sigtype :: 2 byte type of the transient_public_key
           length -> 2 bytes

transient_public_key :: `SigningPublicKey`
                        length -> As inferred from the sigtype

signature :: `Signature`
             length -> As inferred from the sigtype of the signing public key
                       in the `Destination` that preceded this offline signature.
             Signature of expires timestamp, transient sig type, and public key,
             by the destination public key.
```

</details>
#### 설명

* **플래그** (2바이트):
  * 비트 0: 설정된 경우, 오프라인 키가 존재함 ([OfflineSignature](#offlinesignature) 참조)
  * 비트 1: 설정된 경우, 이것은 게시되지 않은 leaseset임
  * 비트 2: 설정된 경우, 이것은 블라인드된 leaseset임
  * 비트 15-3: 예약됨, 0으로 설정

### LeaseSet2Header

#### 목차

이것은 [LeaseSet2](#leaseset2)와 [MetaLeaseSet](#metaleaseset)의 공통 부분입니다. 0.9.38부터 지원되며, 자세한 내용은 proposal 123을 참조하십시오.

#### 참고사항

[Destination](#destination), 두 개의 타임스탬프, 그리고 선택적인 [OfflineSignature](#offlinesignature)를 포함합니다.

```bytefield
destination          | 8 | blue   | Destination, >= 387+ bytes

published            | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
expires              | 2 | cyan   | 2 byte time, offset from published in seconds, 18.2 hours max
flags                | 2 | red
offline_signature    | 8 | purple | OfflineSignature, varies, optional (present if flags bit 0 set

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

published :: 4 byte date
             length -> 4 bytes
             Seconds since the epoch, rolls over in 2106.

expires :: 2 byte time
           length -> 2 bytes
           Offset from published timestamp in seconds, 18.2 hours max

flags :: 2 bytes
  Bit order: 15 14 ... 3 2 1 0
  Bit 0: If 0, no offline keys; if 1, offline keys
  Bit 1: If 0, a standard published leaseset.
         If 1, an unpublished leaseset.
  Bit 2: If 0, a standard published leaseset.
         If 1, this unencrypted leaseset will be blinded and encrypted when published.
  Bits 15-3: set to 0 for compatibility with future uses

offline_signature :: `OfflineSignature`
                     length -> varies
                     Optional, only present if bit 0 is set in the flags.
```

</details>
#### 설명

* 전체 크기: 최소 395바이트

* 실제 최대 만료 시간은 [LeaseSet2](#leaseset2)의 경우 약 660초(11분)이고 [MetaLeaseSet](#metaleaseset)의 경우 65535초(전체 18.2시간)입니다.

* [LeaseSet](#leaseset) (1)에는 'published' 필드가 없어서 버전 관리를 위해 
  가장 이른 lease를 검색해야 했습니다. LeaseSet2는 1초 해상도의 'published' 필드를 
  추가합니다. router들은 새로운 leaseset을 floodfill에 전송하는 것을 
  1초보다 훨씬 느린 속도로 제한해야 합니다 (목적지당). 
  이것이 구현되지 않은 경우, 코드는 각각의 새로운 leaseset이 
  이전 것보다 최소 1초 늦은 'published' 시간을 가지도록 보장해야 하며, 
  그렇지 않으면 floodfill이 새로운 leaseset을 저장하거나 전파하지 않을 것입니다.

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := 원하는 서비스의 심볼릭 이름. 반드시 소문자여야 함. 예시: "smtp".
  허용되는 문자는 [a-z0-9-]이며 '-'로 시작하거나 끝날 수 없음.
  [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)나 Linux /etc/services에 정의된 표준 식별자가 있으면 반드시 사용해야 함.
- proto := 원하는 서비스의 전송 프로토콜. 반드시 소문자여야 하며, "tcp" 또는 "udp" 중 하나.
  "tcp"는 스트리밍을 의미하고 "udp"는 응답 가능한 데이터그램을 의미함.
  원시 데이터그램과 datagram2용 프로토콜 지시자는 나중에 정의될 수 있음.
  허용되는 문자는 [a-z0-9-]이며 '-'로 시작하거나 끝날 수 없음.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := 생존 시간, 정수 초. 양의 정수. 예시: "86400".
  최소 86400 (하루)이 권장되며, 자세한 내용은 아래 권장사항 섹션을 참조.
- priority := 대상 호스트의 우선순위, 값이 낮을수록 더 선호됨. 음이 아닌 정수. 예시: "0"
  여러 레코드가 있을 때만 유용하지만, 레코드가 하나뿐이어도 필수.
- weight := 동일한 우선순위를 가진 레코드들의 상대적 가중치. 값이 높을수록 선택될 확률이 높음. 음이 아닌 정수. 예시: "0"
  여러 레코드가 있을 때만 유용하지만, 레코드가 하나뿐이어도 필수.
- port := 서비스를 찾을 I2CP 포트. 음이 아닌 정수. 예시: "25"
  포트 0은 지원되지만 권장되지 않음.
- target := 서비스를 제공하는 목적지의 호스트명 또는 b32. [NAMING](/docs/overview/naming/)에서와 같은 유효한 호스트명. 반드시 소문자여야 함.
  예시: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" 또는 "example.i2p".
  호스트명이 "잘 알려진" 것, 즉 공식 또는 기본 주소록에 있는 것이 아니라면 b32가 권장됨.
- appoptions := 애플리케이션별 임의 텍스트, " " 또는 ","를 포함할 수 없음. 인코딩은 UTF-8.

### LeaseSet2

#### 목차

유형 3의 I2NP DatabaseStore 메시지에 포함됨. 0.9.38 버전부터 지원되며, 자세한 내용은 제안서 123을 참조하세요.

특정 [Destination](#destination)에 대해 현재 승인된 모든 [Lease2](#lease2)와 garlic 메시지를 암호화할 수 있는 [PublicKey](#publickey)를 포함합니다. LeaseSet은 네트워크 데이터베이스에 저장되는 두 가지 구조 중 하나이며 (다른 하나는 [RouterInfo](#routerinfo)), 포함된 [Destination](#destination)의 SHA256 해시 값을 키로 사용합니다.

#### 암호화 키 선호도

[LeaseSet2Header](#leaseset2header) 다음에 옵션이 오고, 그 후 암호화를 위한 하나 이상의 [PublicKey](#publickey), [Lease2](#lease2) 구조체의 개수를 나타내는 [Integer](#integer), 실제 [Lease2](#lease2) 구조체들, 마지막으로 [Destination](#destination)의 [SigningPrivateKey](#signingprivatekey) 또는 일시 키가 이전 바이트들을 서명한 [Signature](#signature)가 온다.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | gray   | Mapping, varies, 2 bytes minimum
numk             | 2 | red    | Integer, 1 byte, number of encryption keys (1 <= numk <= max TBD)
keytype0         | 3 | cyan   | Encryption type of PublicKey, 2 bytes
keylen0          | 3 | cyan   | Length of PublicKey, 2 bytes
encryption_key_0 | 8 | green  | PublicKey, keylen bytes
keytypen         | 4 | cyan   | Encryption type of PublicKey, 2 bytes
keylenn          | 4 | cyan   | Length of PublicKey, 2 bytes
encryption_key_n | 8 | green  | PublicKey, keylen bytes
num              | 1 | red    | Integer, 1 byte, number of Lease2s (0-16)
Lease2 0         | 7 | yellow | Lease2, 40 bytes
Lease2 ($num-1)  | 8 | yellow | Lease2, 40 bytes
signature        | 8 | purple | Signature, 40 bytes or as specified in destination's key cert
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

numk :: `Integer`
        length -> 1 byte
        Number of key types, key lengths, and `PublicKey`s to follow
        value: 1 <= numk <= max TBD

keytype :: The encryption type of the `PublicKey` to follow.
           length -> 2 bytes

keylen :: The length of the `PublicKey` to follow.
          Must match the specified length of the encryption type.
          length -> 2 bytes

encryption_key :: `PublicKey`
                  length -> keylen bytes

num :: `Integer`
       length -> 1 byte
       Number of `Lease2`s to follow
       value: 0 <= num <= 16

leases :: [`Lease2`]
          length -> $num*40 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header
```

</details>
#### 옵션

게시된(서버) leaseSet의 경우, 암호화 키들은 서버 선호도 순으로 배열되며, 가장 선호되는 것이 먼저 옵니다. 클라이언트가 둘 이상의 암호화 유형을 지원하는 경우, 서버의 선호도를 존중하여 서버에 연결할 때 사용할 암호화 방법으로 지원되는 첫 번째 유형을 선택하는 것이 권장됩니다. 일반적으로 더 새로운(번호가 높은) 키 유형들이 더 안전하거나 효율적이어서 선호되므로, 키들은 키 유형의 역순으로 나열되어야 합니다.

그러나 클라이언트는 구현 방식에 따라 사용자의 선호에 기반하여 선택하거나, "통합된" 선호를 결정하기 위한 어떤 방법을 사용할 수 있습니다. 이것은 설정 옵션으로 사용하거나 디버깅에 유용할 수 있습니다.

게시되지 않은 (클라이언트) leaseSet에서 키 순서는 실질적으로 중요하지 않습니다. 게시되지 않은 클라이언트에 대한 연결은 일반적으로 시도되지 않기 때문입니다. 위에서 설명한 바와 같이 이 순서가 결합된 선호도를 결정하는 데 사용되는 경우를 제외하고는 말입니다.

#### 참고 사항

API 0.9.66부터 서비스 레코드 옵션에 대한 표준 형식이 정의되었습니다. 자세한 내용은 제안서 167을 참조하세요. 다른 형식을 사용하는 서비스 레코드 이외의 옵션은 향후 정의될 수 있습니다.

LS2 옵션은 키로 정렬되어야 하므로 서명이 불변입니다.

서비스 기록 옵션은 다음과 같이 정의됩니다:

* 목적지의 공개 키는 버전 0.6에서 비활성화된 이전 I2CP-to-I2CP 암호화에 사용되었으며, 현재는 사용되지 않습니다.

예시:

LS2에서 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p가 하나의 SMTP 서버를 가리키는 경우:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

LS2에서 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p가 두 개의 SMTP 서버를 가리키는 경우:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p의 LS2에서 자체를 SMTP 서버로 가리킬 경우:

"_smtp._tcp" "0 999999 25"

#### 설명

* 암호화 키는 종단 간 ElGamal/AES+SessionTag 암호화 
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (타입 0) 또는 기타 종단 간 암호화 방식에 사용됩니다.
  [ECIES](/docs/specs/ecies/) 및 제안 145, 156을 참조하십시오.
  이 키들은 router 시작 시마다 새로 생성되거나 지속적으로 유지될 수 있습니다.
  X25519 (타입 4, [ECIES](/docs/specs/ecies/) 참조)는 릴리스 0.9.44부터 지원됩니다.

* 서명은 위의 데이터에 DatabaseStore 타입(3)을 포함하는 단일 바이트를 앞에 붙인(PREPENDED) 것에 대한 것입니다.

* 서명은 목적지의 서명 공개키 또는 leaseset2 헤더에 오프라인 서명이 포함되어 있는 경우 임시 서명 공개키를 사용하여 검증할 수 있습니다.

* 각 키에 대해 키 길이가 제공되므로, floodfill과 클라이언트가 모든 암호화 타입을 알지 못하거나 지원하지 않더라도 구조를 파싱할 수 있습니다.

* [LeaseSet2Header](#leaseset2header)의 'published' 필드에 대한 참고사항을 참조하세요

* 크기가 1보다 큰 경우, 옵션 매핑은 키로 정렬되어야 하므로 서명이 불변입니다.

* 총 크기: 40바이트

JavaDoc: [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### 목차

예비. 완전히 지원되지 않음.

특정 tunnel이 [Destination](#destination)을 대상으로 하는 메시지를 수신할 수 있는 권한을 정의합니다. [Lease2](#lease2)와 동일하지만 tunnel id 대신 플래그와 비용을 사용합니다. [MetaLeaseSet](#metaleaseset)에서 사용됩니다. 타입 7의 I2NP DatabaseStore 메시지에 포함됩니다. 0.9.38부터 지원됩니다. 자세한 정보는 proposal 123을 참조하세요.

#### 참고 사항

게이트웨이 라우터의 [RouterIdentity](#routeridentity)에 대한 SHA256 [Hash](#hash), 그 후 플래그와 비용, 마지막으로 4바이트의 종료 날짜.

```bytefield
tunnel_gw | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes
flags     | 3 | red    | 3 bytes
cost      | 1 | green  | 1 byte
end_date  | 4 | yellow | 4 bytes, seconds since epoch
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway,
             or the hash of another `MetaLeaseSet`.
             length -> 32 bytes

flags :: 3 bytes of flags
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Type of the entry.
         If 0, unknown.
         If 1, a `LeaseSet`.
         If 3, a `LeaseSet2`.
         If 5, a `MetaLeaseSet`.
         Bits 23-4: set to 0 for compatibility with future uses
         length -> 3 bytes

cost :: 1 byte, 0-255. Lower value is higher priority.
        length -> 1 byte

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.

```
</details>
#### 설명

* 목적지의 공개 키는 버전 0.6에서 비활성화된 구 I2CP-to-I2CP 암호화에 사용되었으며, 현재는 사용되지 않습니다.

JavaDoc: [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### 목차

예비. 완전히 지원되지 않음.

유형 7의 I2NP DatabaseStore 메시지에 포함됨. 0.9.38 버전부터 정의되었으며, 자세한 내용은 제안서 123을 참조하세요.

특정 [Destination](#destination)에 대해 현재 승인된 모든 [MetaLease](#metalease)와 마늘 암호화(garlic encryption) 메시지를 암호화할 수 있는 [PublicKey](#publickey)를 포함한다. LeaseSet은 네트워크 데이터베이스(netDb)에 저장되는 두 가지 구조 중 하나이며(다른 하나는 [RouterInfo](#routerinfo)), 포함된 [Destination](#destination)의 SHA256 해시값을 키로 사용한다.

#### 참고사항

[LeaseSet2Header](#leaseset2header)에 이어, 집합에 포함된 [Lease2](#lease2) 구조체의 개수를 나타내는 옵션 [Integer](#integer) 값, 실제 [Lease2](#lease2) 구조체들, 그리고 마지막으로 [Destination](#destination)의 [SigningPrivateKey](#signingprivatekey) 또는 일시적 키가 이전 바이트들을 서명한 [Signature](#signature)가 온다.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | green  | Mapping, varies, 2 bytes minimum
num              | 1 | red    | Integer, 1 byte
MetaLease 0      | 7 | yellow | 40 bytes
MetaLease ($num-1) | 8 | yellow | 40 bytes
numr             | 1 | red    | Integer, 1 byte
revocation_0     | 8 | cyan   | Hash, 32 bytes
revocation_n     | 8 | cyan   | Hash, 32 bytes
signature        | 8 | purple | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

num :: `Integer`
        length -> 1 byte
        Number of `MetaLease`s to follow
        value: 1 <= num <= max TBD

leases :: `MetaLease`s
          length -> $numr*40 bytes

numr :: `Integer`
        length -> 1 byte
        Number of `Hash`es to follow
        value: 0 <= numr <= max TBD

revocations :: [`Hash`]
               length -> $numr*32 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header

```
</details>
#### 설명

* 서명은 위의 데이터에 DatabaseStore 타입(7)을 포함하는 단일 바이트가 앞에 붙은 상태로 적용됩니다.

* 서명은 destination의 서명 공개 키를 사용하거나, leaseset2 헤더에 오프라인 서명이 포함된 경우 임시 서명 공개 키를 사용하여 검증할 수 있습니다.

* [LeaseSet2Header](#leaseset2header)의 'published' 필드에 대한 참고사항을 참조하세요

* destination의 공개 키는 버전 0.6에서 비활성화된 기존 I2CP-to-I2CP 암호화에 사용되었으며, 현재는 사용되지 않습니다.

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### 목차

유형 5의 I2NP DatabaseStore 메시지에 포함되어 있습니다. 0.9.38 버전부터 정의되었으며, 0.9.39 버전부터 작동합니다. 자세한 내용은 제안서 123을 참조하세요.

평문으로는 블라인드 키와 만료 시간만 볼 수 있으며, 실제 리스 세트는 암호화되어 있습니다.

#### 참고사항

2바이트의 서명 유형, 블라인드 처리된 [SigningPrivateKey](#signingprivatekey), 게시 시간, 만료 시간 및 플래그. 그 후, 2바이트 길이 정보와 암호화된 데이터가 뒤따른다. 마지막으로 블라인드 처리된 [SigningPrivateKey](#signingprivatekey) 또는 일시적 키로 서명된 이전 바이트들의 [Signature](#signature)가 온다.

```bytefield
sigtype            | 2 | red    | 2 bytes
blinded_public_key | 8 | blue   | SigningPublicKey, varies
published          | 4 | green  | 4 bytes, seconds since epoch
expires            | 2 | yellow | 2 bytes
flags              | 2 | red    | 2 bytes
offline_signature  | 8 | orange | OfflineSignature, optional, varies
len                | 2 | gray   | Integer, 2 bytes
encrypted_data     | 8 | cyan   | Encrypted data, len bytes
signature          | 8 | purple | Signature, varies
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### 설명

* 서명은 위의 데이터에 DatabaseStore 타입(5)을 포함하는 단일 바이트를 앞에 붙인 것에 대해 적용됩니다.

* 서명은 목적지의 서명 공개 키를 사용하거나, leaseSet2 헤더에 오프라인 서명이 포함된 경우 임시 서명 공개 키를 사용하여 검증할 수 있습니다.

* Blinding과 암호화는 [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)에 명시되어 있습니다

* 이 구조는 [LeaseSet2Header](#leaseset2header)를 사용하지 않습니다.

* 실제 최대 만료 시간은 약 660(11분)이며, 암호화된 [MetaLeaseSet](#metaleaseset)이 아닌 경우입니다.

* 암호화된 leaseSet과 함께 오프라인 서명을 사용하는 방법에 대한 참고사항은 제안서 123을 참조하세요.

* [LeaseSet2Header](#leaseset2header)의 'published' 필드에 대한 참고사항을 참조하세요
  (여기서는 LeaseSet2Header 형식을 사용하지 않지만 동일한 문제입니다)

* 비용은 일반적으로 SSU의 경우 5 또는 6이고, NTCP의 경우 10 또는 11입니다.

* Expiration은 현재 사용되지 않으며, 항상 null(모든 비트가 0)입니다. 릴리스 0.9.3부터 expiration은 0으로 가정되고 저장되지 않으므로, 0이 아닌 expiration 값은 RouterInfo 서명 검증에서 실패합니다. expiration을 구현하거나 이 바이트들을 다른 용도로 사용하는 것은 역호환되지 않는 변경사항이 될 것입니다. Router들은 이 필드를 모두 0으로 설정해야 합니다. 릴리스 0.9.12부터 0이 아닌 expiration 필드가 다시 인식되지만, 네트워크의 대부분이 이를 인식할 때까지 몇 개의 릴리스를 더 기다려야 이 필드를 사용할 수 있습니다.

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### 목차

이 구조는 전송 프로토콜을 통해 라우터에 연결하는 방법을 정의한다.

#### 참고 사항

0은 무료이고 255는 비싸다는 의미인 상대적 비용을 나타내는 1바이트 [정수](#integer) 값, 그리고 이 주소가 더 이상 사용되지 않아야 하는 만료 시점인 [날짜](#date) (null인 경우 만료되지 않음). 그 다음에는 이 라우터 주소가 사용하는 전송 프로토콜을 정의하는 [문자열](#string)이 온다. 마지막으로 연결을 수립하는 데 필요한 전송 방식별 옵션들(예: IP 주소, 포트 번호, 이메일 주소, URL 등)을 포함하는 [매핑](#mapping)이 위치한다.

```bytefield
cost            | 1 | green  | Integer, 1 byte
expiration      | 7 | yellow | Date, 8 bytes
transport_style | 8 | blue   | String, 1-256 bytes
options         | 8 | purple | Mapping
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-/-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### 설명

* 다음 옵션들은 필수는 아니지만 표준이며 대부분의 router 주소에 존재할 것으로 예상됩니다: "host" (IPv4 또는 IPv6 주소나 호스트 이름)와 "port".

* peer_size [Integer](#integer) 다음에는 그만큼의 router 해시 목록이 올 수 있습니다.
  이는 현재 사용되지 않습니다. 제한된 경로의 한 형태를 위해 의도되었으나,
  구현되지 않았습니다.
  특정 구현체에서는 서명이 불변이 되도록 목록이 정렬되어야 할 수 있습니다.
  이 기능을 활성화하기 전에 연구가 필요합니다.

* 서명은 router_ident의 서명 공개 키를 사용하여 검증할 수 있습니다.

* 모든 router 정보에 포함되어야 하는 표준 옵션에 대해서는 네트워크 데이터베이스 페이지 [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)를 참조하세요.

JavaDoc: [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### 목차

router가 네트워크에 공개하고자 하는 모든 데이터를 정의합니다. [RouterInfo](#routerinfo)는 네트워크 데이터베이스에 저장되는 두 구조 중 하나이며(다른 하나는 [LeaseSet](#leaseset)), 포함된 [RouterIdentity](#routeridentity)의 SHA256 해시값을 키로 사용합니다.

#### 참고 사항

[RouterIdentity](#routeridentity) 다음에 이 엔트리가 게시된 [Date](#date)가 옴

```bytefield
router_ident           | 8 | blue   | RouterIdentity, >= 387+ bytes
published              | 8 | green  | Date, 8 bytes
size                   | 1 | red    | Integer, 1 byte
RouterAddress 0        | 7 | yellow | varies
RouterAddress 1        | 8 | yellow | varies
RouterAddress ($size-1)| 8 | yellow | varies
psiz                   | 1 | red    | Integer, 1 byte
options                | 7 | purple | Mapping
signature              | 8 | cyan   | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-/-+----+----+----+
|psiz| options                          |
+----+----+----+----+-/-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### 주의사항

* 매우 오래된 router들은 서명이 불변이 되도록 데이터의 SHA256으로 주소를 정렬할 것을 요구했습니다.
  이는 더 이상 필요하지 않으며, 하위 호환성을 위해 구현할 가치가 없습니다.

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)

* 서명은 라우터 식별자(router_ident)의 서명 공개 키를 사용하여 검증할 수 있습니다.

* 모든 라우터 정보에 포함될 것으로 예상되는 표준 옵션은 [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) 네트워크 데이터베이스 페이지를 참조하세요.

* 오래된 라우터는 주소들을 해당 데이터의 SHA256 기준으로 정렬해야 했기 때문에
  서명이 불변(invariant)이 되도록 했습니다.
  이 제약 조건은 더 이상 필요하지 않으며, 하위 호환성을 위해 구현할 가치가 없습니다.

JavaDoc: [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### 배송 지침

터널 메시지 전달 지침은 터널 메시지 명세 [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)에서 정의된다.

Garlic Message Delivery Instructions는 I2NP Message Specification [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)에서 정의됩니다.

## 참조

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)
