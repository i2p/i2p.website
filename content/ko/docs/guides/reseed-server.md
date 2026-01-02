---
title: "I2P 리시드 서버 생성 및 실행"
description: "I2P 리시드 서버를 설정하고 운영하여 새로운 라우터가 네트워크에 참여할 수 있도록 돕는 완전한 가이드"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Reseed 호스트는 I2P 네트워크의 핵심 인프라로, 부트스트랩 과정에서 새로운 router에게 초기 노드 그룹을 제공합니다. 이 가이드는 자체 reseed 서버를 설정하고 운영하는 방법을 안내합니다.

## I2P Reseed 서버란 무엇인가?

I2P 리시드 서버는 다음과 같은 방식으로 새로운 router가 I2P 네트워크에 통합되도록 돕습니다:

- **초기 피어 발견 제공**: 새로운 라우터가 연결할 네트워크 노드의 초기 집합을 받습니다
- **부트스트랩 복구**: 연결 유지에 어려움을 겪는 라우터를 지원합니다
- **안전한 배포**: 리시딩 프로세스는 네트워크 보안을 보장하기 위해 암호화되고 디지털 서명됩니다

새로운 I2P router가 처음 시작될 때(또는 모든 피어 연결을 잃었을 때), 초기 router 정보 세트를 다운로드하기 위해 reseed 서버에 접속합니다. 이를 통해 새로운 router는 자체 netDb를 구축하고 tunnel을 설정할 수 있습니다.

## 사전 요구 사항

시작하기 전에 필요한 사항:

- root 액세스 권한이 있는 Linux 서버 (Debian/Ubuntu 권장)
- 서버를 가리키는 도메인 이름
- 최소 1GB RAM 및 10GB 디스크 공간
- network database를 채우기 위해 서버에서 실행 중인 I2P router
- Linux 시스템 관리에 대한 기본 지식

## 서버 준비하기

### Step 1: Update System and Install Dependencies

먼저 시스템을 업데이트하고 필요한 패키지를 설치하세요:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
이것은 다음을 설치합니다: - **golang-go**: Go 프로그래밍 언어 런타임 - **git**: 버전 관리 시스템 - **make**: 빌드 자동화 도구 - **docker.io & docker-compose**: Nginx Proxy Manager 실행을 위한 컨테이너 플랫폼

![필요한 패키지 설치](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

reseed-tools 저장소를 복제하고 애플리케이션을 빌드하세요:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
`reseed-tools` 패키지는 reseed 서버 실행을 위한 핵심 기능을 제공합니다. 다음을 처리합니다: - 로컬 netDb에서 router 정보 수집 - router info를 서명된 SU3 파일로 패키징 - HTTPS를 통해 이러한 파일 제공

![reseed-tools 저장소 복제하기](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

reseed 서버의 SSL 인증서와 개인 키를 생성하세요:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**중요한 매개변수**: - `--signer`: 귀하의 이메일 주소 (`admin@stormycloud.org`를 자신의 이메일로 교체) - `--netdb`: I2P router의 네트워크 데이터베이스 경로 - `--port`: 내부 포트 (8443 권장) - `--ip`: localhost에 바인딩 (공개 접근을 위해 리버스 프록시 사용 예정) - `--trustProxy`: 리버스 프록시로부터의 X-Forwarded-For 헤더 신뢰

이 명령은 다음을 생성합니다: - SU3 파일 서명을 위한 개인 키 - 안전한 HTTPS 연결을 위한 SSL 인증서

![SSL 인증서 생성](/images/guides/reseed/reseed_03.png)

### 1단계: 시스템 업데이트 및 의존성 설치

**중요**: `/home/i2p/.reseed/`에 있는 생성된 키를 안전하게 백업하세요:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
이 백업을 제한된 접근 권한이 있는 안전하고 암호화된 위치에 저장하세요. 이 키들은 reseed 서버 운영에 필수적이며 신중하게 보호해야 합니다.

## Configuring the Service

### 2단계: Reseed 도구 복제 및 빌드

systemd 서비스를 생성하여 reseed 서버를 자동으로 실행하세요:

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**반드시 `admin@stormycloud.org`를** 본인의 이메일 주소로 교체하세요.

이제 서비스를 활성화하고 시작합니다:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
서비스가 실행 중인지 확인하세요:

```bash
sudo systemctl status reseed
```
![reseed 서비스 상태 확인](/images/guides/reseed/reseed_04.png)

### 단계 3: SSL 인증서 생성

최적의 성능을 위해 라우터 정보를 새로 고치기 위해 reseed 서비스를 주기적으로 재시작하는 것이 좋습니다:

```bash
sudo crontab -e
```
서비스를 3시간마다 재시작하려면 다음 줄을 추가하세요:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

reseed 서버는 localhost:8443에서 실행되며 공개 HTTPS 트래픽을 처리하기 위해 리버스 프록시가 필요합니다. 사용 편의성을 위해 Nginx Proxy Manager를 권장합니다.

### 4단계: 키 백업하기

Docker를 사용하여 Nginx Proxy Manager 배포:

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
이것은 다음을 노출합니다: - **포트 80**: HTTP 트래픽 - **포트 81**: 관리자 인터페이스 - **포트 443**: HTTPS 트래픽

### Configure Proxy Manager

1. `http://your-server-ip:81`에서 관리자 인터페이스에 접속합니다

2. 기본 자격 증명으로 로그인:
   - **이메일**: admin@example.com
   - **비밀번호**: changeme

**중요**: 최초 로그인 후 즉시 이 인증 정보를 변경하세요!

![Nginx Proxy Manager 로그인](/images/guides/reseed/reseed_05.png)

3. **Proxy Hosts**로 이동하여 **Add Proxy Host**를 클릭합니다

![프록시 호스트 추가](/images/guides/reseed/reseed_06.png)

4. 프록시 호스트 설정:
   - **Domain Name**: 리시드 도메인 (예: `reseed.example.com`)
   - **Scheme**: `https`
   - **Forward Hostname / IP**: `127.0.0.1`
   - **Forward Port**: `8443`
   - **Cache Assets** 활성화
   - **Block Common Exploits** 활성화
   - **Websockets Support** 활성화

![프록시 호스트 세부 정보 구성](/images/guides/reseed/reseed_07.png)

5. **SSL** 탭에서:
   - **Request a new SSL Certificate** (Let's Encrypt) 선택
   - **Force SSL** 활성화
   - **HTTP/2 Support** 활성화
   - Let's Encrypt 서비스 약관 동의

![SSL 인증서 구성](/images/guides/reseed/reseed_08.png)

6. **저장** 클릭

이제 리시드 서버가 `https://reseed.example.com`에서 접근 가능해야 합니다

![성공적인 reseed 서버 구성](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

reseed 서버가 작동하면 I2P 개발자에게 연락하여 공식 reseed 서버 목록에 추가되도록 하세요.

### 5단계: Systemd 서비스 생성

**zzz** (I2P 수석 개발자)에게 다음 정보를 이메일로 보내세요:

- **I2P 이메일**: zzz@mail.i2p
- **일반 인터넷 이메일**: zzz@i2pmail.org

### 6단계: 선택 사항 - 주기적 재시작 구성

이메일에 다음을 포함하세요:

1. **Reseed 서버 URL**: 전체 HTTPS URL (예: `https://reseed.example.com`)
2. **공개 reseed 인증서**: `/home/i2p/.reseed/`에 위치 (`.crt` 파일 첨부)
3. **연락처 이메일**: 서버 유지보수 알림을 위한 선호하는 연락 방법
4. **서버 위치**: 선택 사항이지만 유용함 (국가/지역)
5. **예상 가동 시간**: 서버 유지에 대한 귀하의 약속

### Verification

I2P 개발자들은 귀하의 리시드 서버가 다음을 충족하는지 확인할 것입니다: - 적절히 구성되어 있고 router 정보를 제공하고 있는지 - 유효한 SSL 인증서를 사용하고 있는지 - 올바르게 서명된 SU3 파일을 제공하고 있는지 - 접근 가능하고 응답하는지

승인되면, 귀하의 리시드 서버가 I2P router와 함께 배포되는 목록에 추가되어 새로운 사용자들이 네트워크에 참여하는 데 도움이 됩니다!

## Monitoring and Maintenance

### Nginx Proxy Manager 설치

reseed 서비스를 모니터링하세요:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### 프록시 관리자 구성

시스템 리소스를 주시하세요:

```bash
htop
df -h
```
### Update Reseed Tools

최신 개선 사항을 받기 위해 주기적으로 reseed-tools를 업데이트하세요:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### 연락처 정보

Nginx Proxy Manager를 통해 Let's Encrypt를 사용하는 경우, 인증서가 자동으로 갱신됩니다. 갱신이 정상적으로 작동하는지 확인하세요:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## 서비스 구성

### 필수 정보

오류 확인을 위한 로그 검사:

```bash
sudo journalctl -u reseed -n 50
```
일반적인 문제: - I2P router가 실행되지 않았거나 netDb가 비어있음 - 8443 포트가 이미 사용 중 - `/home/i2p/.reseed/` 디렉토리에 대한 권한 문제

### 검증

I2P router가 실행 중이고 네트워크 데이터베이스가 채워져 있는지 확인하세요:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
많은 `.dat` 파일들이 보일 것입니다. 비어있다면, I2P router가 피어를 발견할 때까지 기다리세요.

### SSL Certificate Errors

인증서가 유효한지 확인하세요:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### 서비스 상태 확인

확인: - DNS 레코드가 서버를 올바르게 가리키고 있는지 - 방화벽이 80번과 443번 포트를 허용하는지 - Nginx Proxy Manager가 실행 중인지: `docker ps`

## Security Considerations

- **개인 키 보안 유지**: `/home/i2p/.reseed/` 내용을 절대 공유하거나 노출하지 마세요
- **정기 업데이트**: 시스템 패키지, Docker, reseed-tools를 최신 상태로 유지하세요
- **로그 모니터링**: 의심스러운 접근 패턴을 주시하세요
- **속도 제한**: 남용 방지를 위해 속도 제한 구현을 고려하세요
- **방화벽 규칙**: 필요한 포트만 노출하세요 (80, 443, 81은 관리자용)
- **관리자 인터페이스**: Nginx Proxy Manager 관리자 인터페이스(포트 81)를 신뢰할 수 있는 IP로만 제한하세요

## Contributing to the Network

reseed 서버를 운영함으로써, 당신은 I2P 네트워크를 위한 중요한 인프라를 제공하고 있습니다. 더 프라이빗하고 탈중앙화된 인터넷에 기여해 주셔서 감사합니다!

질문이나 도움이 필요하시면 I2P 커뮤니티에 문의하세요: - **포럼**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: 다양한 네트워크의 #i2p - **개발**: [i2pgit.org](https://i2pgit.org)

---


*가이드는 원래 [Stormy Cloud](https://www.stormycloud.org)에 의해 작성되었으며, I2P 문서를 위해 수정되었습니다.*
