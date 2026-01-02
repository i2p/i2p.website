---
title: "Reseed Hosts (I2P 네트워크에 처음 연결할 때 필요한 초기 네트워크 정보를 배포하는 호스트)"
description: "reseed 서비스(초기 부트스트랩 서비스) 운영 및 대체 부트스트랩 방법"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Reseed 호스트(초기 부트스트랩 서버) 소개

새로운 router가 I2P 네트워크에 참여하려면 소수의 피어가 필요합니다. reseed(초기 피어 확보) 호스트는 암호화된 HTTPS 다운로드를 통해 그 초기 부트스트랩 세트를 제공합니다. 각 reseed 번들은 호스트가 서명하여 인증되지 않은 주체의 변조를 방지합니다. 안정적으로 동작하는 router도 피어 집합이 오래되어 활성도가 떨어지면 가끔 reseed할 수 있습니다.

### 네트워크 부트스트랩 절차

처음으로 I2P router를 시작하거나 오랜 기간 오프라인이었던 경우, 네트워크에 연결하려면 RouterInfo(라우터 정보) 데이터가 필요합니다. router에는 기존 피어가 없기 때문에, I2P 네트워크 내부만으로는 이 정보를 얻을 수 없습니다. reseed mechanism(재시드 메커니즘: 초기 부트스트랩 절차)은 신뢰할 수 있는 외부 HTTPS 서버에서 제공되는 RouterInfo 파일을 통해 이러한 부트스트랩 문제를 해결합니다.

reseed(초기 부트스트랩) 과정은 암호학적으로 서명된 단일 번들로 75-100개의 RouterInfo 파일을 전달한다. 이는 새로운 routers가 별개의 신뢰할 수 없는 네트워크 파티션으로 고립시킬 수 있는 중간자 공격에 노출되지 않으면서 신속하게 연결을 설정할 수 있도록 보장한다.

### 현재 네트워크 상태

2025년 10월 기준, I2P 네트워크는 router 버전 2.10.0(API 버전 0.9.67)으로 운영된다. 버전 0.9.14에서 도입된 reseed protocol(초기 부트스트랩 프로토콜)은 안정적이며 핵심 기능에는 변화가 없다. 네트워크는 가용성과 검열 저항성을 보장하기 위해 전 세계에 분산된 다수의 독립적인 reseed 서버를 유지한다.

서비스 [checki2p](https://checki2p.com/reseed)는 모든 I2P reseed 서버(초기 부트스트랩을 위한 router 정보 배포 서버)를 4시간마다 모니터링하며, reseed 인프라의 실시간 상태 점검과 가용성 지표를 제공합니다.

## SU3 파일 형식 사양

SU3 파일 형식은 암호학적으로 서명된 콘텐츠 배포를 제공하는 I2P의 reseed(네트워크 부트스트랩) 프로토콜의 기반입니다. 이 형식을 이해하는 것은 reseed 서버와 클라이언트를 구현하는 데 필수적입니다.

### 파일 구조

SU3 형식은 세 가지 주요 구성 요소로 이루어져 있습니다: 헤더(40바이트 이상), 콘텐츠(가변 길이), 서명(헤더에서 지정된 길이).

#### 헤더 형식(바이트 0-39 최소)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Reseed(리시드: I2P 네트워크 부트스트랩 서버) 전용 SU3 매개변수

reseed bundles(초기 부트스트랩용 피어 목록 묶음)의 경우, SU3 파일은 다음 요건을 충족해야 합니다:

- **파일 이름**: 반드시 정확히 `i2pseeds.su3`여야 합니다
- **콘텐츠 유형** (바이트 27): 0x03 (RESEED)
- **파일 유형** (바이트 25): 0x00 (ZIP)
- **서명 유형** (바이트 8-9): 0x0006 (RSA-4096-SHA512)
- **버전 문자열**: ASCII의 Unix timestamp (epoch(에포크) 이후의 초, date +%s 형식)
- **서명자 ID**: X.509 인증서의 CN(공통 이름)과 일치하는 이메일 형태의 식별자

#### 네트워크 ID 쿼리 매개변수

버전 0.9.42부터 routers는 reseed 요청(초기 부트스트랩용 피어 목록을 받아오는 요청)에 `?netid=2`를 덧붙입니다. 이는 테스트 네트워크가 서로 다른 네트워크 ID를 사용하므로 교차 네트워크 연결을 방지합니다. 현재 I2P 운영 네트워크는 네트워크 ID 2를 사용합니다.

예시 요청: `https://reseed.example.com/i2pseeds.su3?netid=2`

### ZIP 콘텐츠 구조

콘텐츠 섹션(헤더 이후, 서명 이전)은 다음 요구 사항을 충족하는 표준 ZIP 아카이브를 포함합니다:

- **압축**: 표준 ZIP 압축(DEFLATE)
- **파일 개수**: 보통 RouterInfo 파일 75~100개
- **디렉터리 구조**: 모든 파일은 최상위 경로에 있어야 합니다(하위 디렉터리 없음)
- **파일 이름**: `routerInfo-{44-character-base64-hash}.dat`
- **Base64 알파벳**: I2P의 수정된 base64 알파벳을 사용해야 합니다

I2P base64 알파벳은 표준 base64와 달리 파일 시스템 및 URL 호환성을 보장하기 위해 `+`와 `/` 대신 `-`와 `~`를 사용합니다.

### 암호학적 서명

서명은 바이트 0부터 콘텐츠 섹션의 끝까지 파일 전체를 대상으로 합니다. 서명 자체는 콘텐츠 뒤에 덧붙여집니다.

#### 서명 알고리즘 (RSA-4096-SHA512)

1. 바이트 0부터 콘텐츠 끝까지의 SHA-512 해시를 계산합니다
2. "raw" RSA를 사용하여 해시에 서명합니다(Java 용어로는 NONEwithRSA)
3. 필요한 경우 선행 0으로 서명을 패딩하여 512바이트가 되도록 합니다
4. 512바이트 서명을 파일 끝에 추가합니다

#### 서명 검증 프로세스

클라이언트는 다음을 수행해야 합니다:

1. 서명 유형과 길이를 판별하기 위해 바이트 0–11을 읽는다
2. 콘텐츠의 경계를 찾기 위해 전체 헤더를 읽는다
3. SHA-512 해시를 계산하는 동안 콘텐츠를 스트리밍한다
4. 파일 끝에서 서명을 추출한다
5. 서명자의 RSA-4096 공개 키를 사용하여 서명을 검증한다
6. 서명 검증이 실패하면 파일을 거부한다

### 인증서 신뢰 모델

Reseed(초기 부트스트랩) 서명자 키는 RSA-4096 키를 사용하는 자체 서명된 X.509 인증서로 배포됩니다. 이러한 인증서는 I2P router 패키지의 `certificates/reseed/` 디렉터리에 포함되어 있습니다.

인증서 형식: - **키 유형**: RSA-4096 - **서명**: 자체 서명 - **Subject CN (공통 이름)**: SU3 헤더의 Signer ID(서명자 ID)와 일치해야 합니다 - **유효 기간**: 클라이언트는 인증서의 유효 기간을 강제해야 합니다

## Reseed(네트워크 부트스트랩 서버) 호스트 운영

reseed 서비스(신규 참여 routers의 부트스트랩을 돕는 서비스)를 운영하려면 보안, 신뢰성, 그리고 네트워크 다양성 요구사항에 세심한 주의를 기울여야 합니다. 더 많은 독립적인 reseed 호스트는 복원력을 높이고, 공격자나 검열자가 새로운 routers의 참여를 차단하기 더 어렵게 만듭니다.

### 기술 요구 사항

#### 서버 사양

- **운영 체제**: Unix/Linux (Ubuntu, Debian, FreeBSD는 테스트 완료 및 권장)
- **네트워크 연결**: 정적 IPv4 주소 필수, IPv6 권장(선택 사항)
- **CPU**: 최소 2코어
- **RAM**: 최소 2GB
- **대역폭**: 월 약 15GB 트래픽
- **가동 시간**: 24/7 운영 필수
- **I2P Router**: 시스템에 잘 통합되어 상시 실행되는 I2P router

#### 소프트웨어 요구 사항

- **Java**: JDK 8 이상 (I2P 2.11.0부터는 Java 17+가 필요함)
- **웹 서버**: 리버스 프록시 지원을 갖춘 nginx 또는 Apache (X-Forwarded-For 헤더의 제한으로 인해 Lighttpd는 더 이상 지원되지 않음)
- **TLS/SSL**: 유효한 TLS 인증서 (Let's Encrypt, 자체 서명 인증서, 또는 상용 CA)
- **DDoS 보호**: fail2ban 또는 동등한 도구 (필수, 선택 사항 아님)
- **Reseed Tools**: https://i2pgit.org/idk/reseed-tools의 공식 reseed-tools(네트워크 부트스트랩용 도구)

### 보안 요구사항

#### HTTPS/TLS 구성

- **프로토콜**: HTTPS만, HTTP 폴백(fallback) 없음
- **TLS 버전**: 최소 TLS 1.2
- **암호 스위트**: Java 8+와 호환되는 강력한 암호 스위트를 지원해야 함
- **인증서 CN/SAN**: 제공되는 URL 호스트명과 일치해야 함 (CN/SAN은 인증서의 Common Name과 Subject Alternative Name을 의미)
- **인증서 유형**: 개발팀과 협의된 경우 self-signed(자체 서명) 가능, 또는 인정된 CA(인증 기관)가 발급한 인증서

#### 인증서 관리

SU3 서명 인증서와 TLS 인증서는 서로 다른 목적을 수행한다:

- **TLS 인증서** (`certificates/ssl/`): HTTPS 통신을 보호합니다
- **SU3 서명 인증서** (`certificates/reseed/`): reseed 번들(I2P 네트워크 초기화용 번들)에 서명합니다

두 인증서는 router 패키지에 포함되도록 reseed coordinator(리시드 담당자)(zzz@mail.i2p)에게 제출되어야 합니다.

#### DDoS 및 스크레이핑 보호

Reseed servers(네트워크 초기 부트스트랩용 서버)는 버그가 있는 구현, 봇넷, 그리고 네트워크 데이터베이스를 스크래핑하려는 악의적 행위자들로부터 주기적인 공격에 직면합니다. 보호 조치는 다음과 같습니다:

- **fail2ban**: 요청 속도 제한과 공격 완화를 위해 필수
- **Bundle 다양성**: 서로 다른 요청자에게 서로 다른 RouterInfo(라우터 정보) 집합을 제공
- **Bundle 일관성**: 구성 가능한 시간 창 내에서 동일 IP의 반복 요청에는 동일한 번들을 제공
- **IP 로깅 제한**: 로그나 IP 주소를 공개하지 말 것(개인정보 보호정책 요구사항)

### 구현 방법

#### 방법 1: 공식 reseed-tools (권장)

I2P 프로젝트에서 관리하는 공식 구현입니다. 저장소: https://i2pgit.org/idk/reseed-tools

**설치**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
첫 실행 시, 도구는 다음을 생성합니다: - `your-email@mail.i2p.crt` (SU3 서명용 인증서) - `your-email@mail.i2p.pem` (SU3 서명용 개인 키) - `your-email@mail.i2p.crl` (인증서 폐지 목록) - TLS 인증서 및 키 파일

**기능**: - 자동 SU3 번들 생성(350가지 변형, 각 변형당 RouterInfos 77개) - 내장 HTTPS 서버 - cron을 통해 9시간마다 캐시 재빌드 - `--trustProxy` 플래그와 함께 X-Forwarded-For 헤더 지원 - 리버스 프록시 구성과 호환

**운영 환경 배포**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### 방법 2: Python 구현 (pyseeder)

PurpleI2P 프로젝트의 대체 구현: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### 방법 3: Docker 배포

컨테이너화된 환경에서는 Docker에 바로 사용할 수 있는 구현이 여러 가지 있습니다:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Tor 오니온 서비스 및 IPFS 지원을 추가

### 역방향 프록시 구성

#### nginx 설정

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Apache 설정

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### 등록 및 조정

공식 I2P 패키지에 귀하의 reseed 서버(초기 부트스트랩용 서버)를 포함하려면:

1. 설정 및 테스트를 완료하세요
2. 두 인증서(SU3 signing 및 TLS)를 reseed coordinator(리시드 조정자)에게 보내세요
3. 연락처: zzz@mail.i2p 또는 zzz@i2pmail.org
4. 다른 운영자들과의 조정을 위해 IRC2P의 #i2p-dev에 참여하세요

### 운영 모범 사례

#### 모니터링 및 로깅

- 통계를 위해 Apache/nginx의 combined 로그 형식을 활성화하세요
- 로그 로테이션을 설정하세요(로그가 빠르게 증가합니다)
- 번들 생성 성공 여부와 재빌드 소요 시간을 모니터링하세요
- 대역폭 사용량과 요청 패턴을 추적하세요
- IP 주소나 상세 접속 로그를 절대 공개하지 마세요

#### 유지보수 일정

- **9시간마다**: SU3 번들 캐시 재생성 (cron으로 자동화)
- **매주**: 로그를 검토하여 공격 패턴 식별
- **매월**: I2P router 및 reseed-tools 업데이트
- **필요 시**: TLS 인증서 갱신 (Let's Encrypt로 자동화)

#### 포트 선택

- 기본: 8443 (권장)
- 대안: 1024-49151 사이의 임의의 포트
- 포트 443: 루트 권한 또는 포트 포워딩이 필요함 (iptables redirect 권장)

포트 포워딩 예시:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## 대체 Reseed(초기 피어 데이터 가져오기) 방법

다른 부트스트랩 옵션은 제한적인 네트워크 환경에 있는 사용자에게 도움이 됩니다:

### 파일 기반 Reseed(네트워크 초기 부트스트랩)

버전 0.9.16에서 도입된 파일 기반 reseeding(재시드: 초기 피어 정보를 받아 네트워크에 합류하는 과정)은 사용자가 RouterInfo 번들을 수동으로 로드할 수 있게 해줍니다. 이 방법은 HTTPS reseed 서버가 차단된 검열 지역의 사용자에게 특히 유용합니다.

**프로세스**: 1. 신뢰할 수 있는 연락처가 자신의 router를 사용해 SU3 bundle(서명된 번들 파일)을 생성한다 2. 번들은 이메일, USB 드라이브 또는 기타 out-of-band 채널(본 채널과 분리된 별도 경로)을 통해 전송된다 3. 사용자는 `i2pseeds.su3`를 I2P 구성 디렉터리에 배치한다 4. Router는 재시작 시 번들을 자동으로 감지하고 처리한다

**문서**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**사용 사례**: - reseed servers(I2P 네트워크 초기 접속을 위한 서버)를 차단하는 국가 방화벽 뒤에 있는 사용자 - 수동 부트스트랩이 필요한 격리된 네트워크 - 테스트 및 개발 환경

### Cloudflare로 프록시된 Reseeding(부트스트랩을 위한 초기 시드 데이터 다운로드 과정)

Cloudflare의 CDN을 통해 reseed(I2P 네트워크 초기 부트스트랩) 트래픽을 라우팅하는 것은 검열이 심한 지역의 운영자들에게 몇 가지 이점을 제공한다.

**이점**: - 클라이언트로부터 오리진 서버 IP 주소를 숨김 - Cloudflare의 인프라를 통한 DDoS 보호 - 엣지 캐싱을 통한 지리적 부하 분산 - 전 세계 클라이언트를 위한 성능 향상

**구현 요건**: - reseed-tools에서 `--trustProxy` 플래그 활성화 - DNS 레코드에 대해 Cloudflare 프록시 활성화 - 적절한 X-Forwarded-For 헤더 처리

**중요 유의사항**: - Cloudflare 포트 제한이 적용됨(지원되는 포트만 사용해야 함) - 동일 클라이언트 번들의 일관성을 위해 X-Forwarded-For 지원이 필요함 - SSL/TLS 구성은 Cloudflare에서 관리됨

**문서**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### 검열 저항 전략

Nguyen Phong Hoang의 연구(USENIX FOCI 2019)는 검열된 네트워크를 위한 추가적인 부트스트랩 방법을 식별합니다:

#### 클라우드 스토리지 제공업체

- **Box, Dropbox, Google Drive, OneDrive**: 공개 링크로 SU3 파일(서명된 업데이트 파일 형식)을 호스팅
- **장점**: 정상적인 서비스를 방해하지 않고는 차단하기 어렵다
- **제한사항**: 사용자에게 URL을 수동으로 배포해야 한다

#### IPFS 배포

- InterPlanetary File System(IPFS, 분산 콘텐츠 주소형 파일 시스템)에 reseed 번들을 호스팅합니다
- 콘텐츠 주소형 스토리지는 변조를 방지합니다
- 테이크다운(삭제 요청) 시도에 강합니다

#### Tor Onion Services(토르 오니언 서비스)

- .onion 주소를 통해 접근 가능한 Reseed servers(네트워크 초기 부트스트랩 서버)
- IP 기반 차단에 강함
- 사용자의 시스템에 Tor 클라이언트가 필요함

**연구 문서**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### I2P 차단이 확인된 국가

2025년 기준, 다음 국가들은 I2P reseed servers(네트워크 부트스트랩 서버)를 차단하는 것으로 확인되었습니다:
- 중국
- 이란
- 오만
- 카타르
- 쿠웨이트

이들 지역의 사용자는 대체 bootstrap(초기 연결 설정) 방법 또는 검열에 강한 reseeding(초기 피어 정보 가져오기) 전략을 활용해야 합니다.

## 구현자를 위한 프로토콜 세부 사항

### Reseed(리시드) 요청 명세서

#### 클라이언트 동작

1. **서버 선택**: Router는 reseed URL(네트워크 부트스트랩용 서버 URL)의 하드코딩된 목록을 유지
2. **무작위 선택**: 클라이언트가 사용 가능한 목록에서 서버를 무작위로 선택
3. **요청 형식**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: 일반적인 브라우저를 모방해야 함 (예: "Wget/1.11.4")
5. **재시도 로직**: SU3 요청이 실패하면 인덱스 페이지 파싱으로 대체
6. **인증서 검증**: 시스템 신뢰 저장소와 대조하여 TLS 인증서를 검증
7. **SU3 서명 검증**: 알려진 reseed 인증서와 대조하여 서명을 검증

#### 서버 동작

1. **번들 선택**: netDb에서 RouterInfos의 의사무작위 부분집합을 선택
2. **클라이언트 추적**: 소스 IP로 요청을 식별(X-Forwarded-For를 반영)
3. **번들 일관성**: 시간 창 내 반복 요청에는 동일한 번들을 반환(일반적으로 8-12시간)
4. **번들 다양성**: 네트워크 다양성을 위해 서로 다른 클라이언트에 서로 다른 번들을 반환
5. **Content-Type**: `application/octet-stream` 또는 `application/x-i2p-reseed`

### RouterInfo 파일 형식

reseed bundle(리시드 번들)의 각 `.dat` 파일에는 RouterInfo 구조체가 포함되어 있습니다:

**파일 이름 규칙**: `routerInfo-{base64-hash}.dat` - 해시는 I2P base64 alphabet(I2P에서 사용하는 base64 문자 집합)을 사용하며 44자입니다 - 예: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**파일 내용**: - RouterIdentity(라우터 식별 정보) (router 해시, 암호화 키, 서명 키) - 발행 타임스탬프 - Router 주소(IP, 포트, 전송 유형) - Router 기능 및 옵션 - 위의 모든 데이터를 포괄하는 서명

### 네트워크 다양성 요구사항

네트워크 중앙집중화를 방지하고 시빌(Sybil) 공격 탐지를 가능하게 하기 위해:

- **완전한 NetDb 덤프 금지**: 단일 클라이언트에게 모든 RouterInfos(라우터 정보 레코드)를 절대 제공하지 말 것
- **무작위 샘플링**: 각 번들은 사용 가능한 피어의 서로 다른 부분집합을 포함
- **최소 번들 크기**: RouterInfos 75개(기존 50개에서 상향)
- **최대 번들 크기**: RouterInfos 100개
- **신선도**: RouterInfos는 최근(생성 후 24시간 이내)이어야 함

### IPv6 고려 사항

**현재 상태** (2025): - 여러 reseed servers(초기 부트스트랩 서버)에서 IPv6 무응답 현상이 나타남 - 신뢰성을 위해 클라이언트는 IPv4를 우선 사용하거나 강제하는 것이 바람직함 - 새로운 배포에서는 IPv6 지원을 권장하지만 필수는 아님

**구현 참고**: 듀얼 스택 서버를 구성할 때 IPv4와 IPv6 수신 주소가 모두 올바르게 동작하는지 확인하거나, 제대로 지원할 수 없다면 IPv6를 비활성화하십시오.

## 보안 고려사항

### 위협 모델

reseed protocol(네트워크 초기 부트스트랩을 위한 재시드 프로토콜)은 다음으로부터 방어합니다:

1. **중간자 공격**: RSA-4096 서명으로 번들 변조를 방지합니다
2. **네트워크 분할**: 여러 독립적인 reseed 서버(초기 네트워크 부트스트랩용 서버)가 단일 통제 지점을 방지합니다
3. **시빌 공격**: 번들의 다양성이 공격자가 사용자를 고립시키는 능력을 제한합니다
4. **검열**: 여러 서버와 대체 방법이 중복성을 제공합니다

reseed(네트워크 부트스트랩) 프로토콜은 다음에 대해 방어하지 않습니다:

1. **침해된 reseed 서버**: 공격자가 reseed(초기 부트스트랩을 위해 netDb 피어 정보를 내려받는 과정) 인증서 개인 키를 탈취한 경우
2. **네트워크 전면 차단**: 특정 지역에서 모든 reseed 방법이 차단된 경우
3. **장기 모니터링**: reseed 요청은 I2P에 참여하려는 IP를 드러낸다

### 인증서 관리

**개인 키 보안**: - 사용하지 않을 때 SU3 서명 키를 오프라인에 보관 - 키 암호화에 강력한 비밀번호를 사용 - 키와 인증서의 안전한 백업을 유지 - 고가치 자산을 다루는 배포 환경에서는 하드웨어 보안 모듈(HSM) 사용을 고려

**인증서 폐지**: - 인증서 폐지 목록(CRLs)은 뉴스 피드를 통해 배포 - 침해된 인증서는 조정자가 폐지할 수 있음 - Routers는 소프트웨어 업데이트 시 CRLs를 자동으로 업데이트함

### 공격 완화

**DDoS 보호**: - 과도한 요청에 대한 fail2ban 규칙 - 웹 서버 수준에서의 요청률 제한 - IP 주소당 연결 제한 - 추가적인 보호 계층을 위한 Cloudflare 또는 유사한 CDN

**스크레이핑 방지**: - 요청한 IP별 서로 다른 번들 - IP별 시간 기반 번들 캐싱 - 스크레이핑 시도를 시사하는 패턴 로깅 - 탐지된 공격에 대해 다른 운영자들과의 협력

## 테스트 및 검증

### 자신의 Reseed Server(새 router의 부트스트랩에 필요한 초기 netDb 데이터를 제공하는 서버) 테스트하기

#### 방법 1: 새 Router 설치

1. 깨끗한 시스템에 I2P를 설치합니다
2. 구성에 reseed(초기 네트워크 부트스트랩) URL을 추가합니다
3. 다른 reseed URL을 제거하거나 비활성화합니다
4. router를 시작하고 reseed 성공 여부를 로그로 모니터링합니다
5. 5-10분 내에 네트워크 연결을 확인합니다

예상 로그 출력:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### 방법 2: 수동 SU3 유효성 검사

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### 방법 3: checki2p 모니터링

https://checki2p.com/reseed 에 있는 서비스는 모든 등록된 I2P reseed 서버(reseed: 초기 피어 정보를 배포하는 서버)에 대해 4시간마다 자동 점검을 수행합니다. 이는 다음을 제공합니다:

- 가용성 모니터링
- 응답 시간 지표
- TLS 인증서 검증
- SU3 서명 검증
- 가동 시간 이력 데이터

귀하의 reseed(초기 부트스트랩 서버)가 I2P 프로젝트에 등록되면 24시간 이내에 checki2p에 자동으로 표시됩니다.

### 일반적인 문제 해결

**문제**: 첫 실행 시 "Unable to read signing key" - **해결책**: 이는 정상입니다. 새 키를 생성하려면 'y'를 입력하세요.

**문제**: Router가 서명 검증에 실패함 - **원인**: 인증서가 router의 신뢰 저장소에 없음 - **해결 방법**: 인증서를 `~/.i2p/certificates/reseed/` 디렉터리에 두세요

**문제**: 동일한 번들이 서로 다른 클라이언트에 전달됨 - **원인**: X-Forwarded-For 헤더가 제대로 전달되지 않음 - **해결책**: `--trustProxy`를 활성화하고 리버스 프록시 헤더를 구성

**문제**: "Connection refused" 오류 - **원인**: 인터넷에서 포트에 접근할 수 없음 - **해결 방법**: 방화벽 규칙 확인, 포트 포워딩 확인

**문제**: 번들 재빌드 중 높은 CPU 사용률 - **원인**: 350개 이상의 SU3(업데이트 패키지 파일 형식) 변형을 생성할 때의 정상 동작 - **해결책**: 충분한 CPU 자원을 확보하고, 재빌드 빈도 감소를 고려하세요

## 참고 정보

### 공식 문서

- **Reseed(I2P 네트워크 초기 부트스트랩) 기여자 가이드**: /guides/creating-and-running-an-i2p-reseed-server/
- **Reseed 정책 요건**: /guides/reseed-policy/
- **SU3 명세**: /docs/specs/updates/
- **Reseed 도구 저장소**: https://i2pgit.org/idk/reseed-tools
- **Reseed 도구 문서**: https://eyedeekay.github.io/reseed-tools/

### 대안 구현체

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder (I2P 네트워크 초기 피어 배포 서버)**: https://github.com/torbjo/i2p-reseeder

### 커뮤니티 리소스

- **I2P 포럼**: https://i2pforum.net/
- **Gitea 저장소**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: IRC2P의 #i2p-dev
- **상태 모니터링**: https://checki2p.com/reseed

### 버전 이력

- **0.9.14** (2014): SU3 리시드 형식 도입
- **0.9.16** (2014): 파일 기반 리시딩 추가
- **0.9.42** (2019): Network ID 쿼리 매개변수 필수화
- **2.0.0** (2022): SSU2 전송 프로토콜 도입
- **2.4.0** (2024): NetDB 격리 및 보안 개선
- **2.6.0** (2024): I2P-over-Tor 연결 차단
- **2.10.0** (2025): 현재 안정 릴리스(2025년 9월 기준)

### 서명 유형 참조

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Reseed Standard**: reseed(네트워크 초기 부트스트랩) 번들에는 Type 6 (RSA-SHA512-4096)이 필요합니다.

## 감사

네트워크의 접근성과 탄력성을 유지해 주신 모든 reseed(초기 연결을 위한 부트스트랩 서비스) 운영자께 감사드립니다. 다음 기여자와 프로젝트에 특별한 감사를 표합니다:

- **zzz**: 오랜 I2P 개발자이자 reseed(초기 접속을 위해 netDb 정보를 받아오는 부트스트랩 절차) 코디네이터
- **idk**: reseed-tools의 현재 유지관리자이자 릴리스 매니저
- **Nguyen Phong Hoang**: 검열 저항적 reseeding 전략에 대한 연구
- **PurpleI2P Team**: 대체 I2P 구현과 도구
- **checki2p**: reseed 인프라를 위한 자동화된 모니터링 서비스

I2P 네트워크의 분산형 reseed(초기 접속을 위한 피어 정보 배포) 인프라는 전 세계 수십 명의 운영자가 협력한 결과물로, 지역적 검열이나 기술적 장벽과 무관하게 신규 사용자가 언제나 네트워크에 합류할 경로를 찾을 수 있도록 보장한다.
