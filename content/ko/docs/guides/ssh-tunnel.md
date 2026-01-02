---
title: "I2P에 원격으로 접근하기 위한 SSH 터널 생성"
description: "Windows, Linux, Mac에서 안전한 SSH 터널을 생성하여 원격 I2P router에 접근하는 방법을 알아보세요"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SSH 터널은 원격 I2P router의 콘솔이나 다른 서비스에 접근하기 위한 안전하고 암호화된 연결을 제공합니다. 이 가이드는 Windows, Linux, Mac 시스템에서 SSH 터널을 생성하는 방법을 보여줍니다.

## SSH 터널이란 무엇인가?

SSH 터널은 암호화된 SSH 연결을 통해 데이터와 정보를 안전하게 라우팅하는 방법입니다. 인터넷을 통과하는 보호된 "파이프라인"을 만드는 것으로 생각하면 됩니다 - 데이터가 이 암호화된 터널을 통해 이동하므로, 전송 과정에서 누구도 데이터를 가로채거나 읽을 수 없습니다.

SSH 터널링은 특히 다음과 같은 경우에 유용합니다:

- **원격 I2P router 접속**: 원격 서버에서 실행 중인 I2P 콘솔에 연결
- **보안 연결**: 모든 트래픽이 종단 간 암호화됨
- **제한 우회**: 원격 시스템의 서비스를 로컬에 있는 것처럼 접근
- **포트 포워딩**: 로컬 포트를 원격 서비스에 매핑

I2P 환경에서 SSH 터널을 사용하여 원격 서버의 I2P router console(일반적으로 7657 포트)에 접근할 수 있으며, 이를 컴퓨터의 로컬 포트로 포워딩할 수 있습니다.

## 전제 조건

SSH 터널을 생성하기 전에 다음이 필요합니다:

- **SSH 클라이언트**:
  - Windows: [PuTTY](https://www.putty.org/) (무료 다운로드)
  - Linux/Mac: 내장 SSH 클라이언트 (터미널 사용)
- **원격 서버 접근**:
  - 원격 서버의 사용자 이름
  - 원격 서버의 IP 주소 또는 호스트명
  - SSH 비밀번호 또는 키 기반 인증
- **사용 가능한 로컬 포트**: 1-65535 범위에서 사용하지 않는 포트 선택 (I2P의 경우 일반적으로 7657 사용)

## 터널 명령어 이해하기

SSH 터널 명령은 다음과 같은 패턴을 따릅니다:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**파라미터 설명**: - **local_port**: 로컬 머신의 포트 (예: 7657) - **destination_ip**: 일반적으로 `127.0.0.1` (원격 서버의 localhost) - **destination_port**: 원격 서버의 서비스 포트 (예: I2P의 경우 7657) - **username**: 원격 서버의 사용자 이름 - **remote_server**: 원격 서버의 IP 주소 또는 호스트명

**예제**: `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

이는 다음과 같은 터널을 생성합니다: - 로컬 머신의 7657 포트가 전달됩니다... - 원격 서버의 localhost(I2P가 실행 중인 곳)의 7657 포트로 - 서버 `20.228.143.58`에 사용자 `i2p`로 연결

## Windows에서 SSH 터널 생성하기

Windows 사용자는 무료 SSH 클라이언트인 PuTTY를 사용하여 SSH 터널을 생성할 수 있습니다.

### Step 1: Download and Install PuTTY

[putty.org](https://www.putty.org/)에서 PuTTY를 다운로드하여 Windows 시스템에 설치하십시오.

### Step 2: Configure the SSH Connection

PuTTY를 열고 연결을 구성하십시오:

1. **Session** 카테고리에서:
   - **Host Name** 필드에 원격 서버의 IP 주소 또는 호스트명을 입력합니다
   - **Port**가 22(기본 SSH 포트)로 설정되어 있는지 확인합니다
   - Connection type은 **SSH**여야 합니다

![PuTTY 세션 설정](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

왼쪽 사이드바에서 **Connection → SSH → Tunnels**로 이동하세요:

1. **Source port**: 사용할 로컬 포트를 입력합니다 (예: `7657`)
2. **Destination**: `127.0.0.1:7657`을 입력합니다 (원격 서버의 localhost:port)
3. **Add**를 클릭하여 터널을 추가합니다
4. "Forwarded ports" 목록에 터널이 표시되어야 합니다

![PuTTY 터널 구성](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. **Open**을 클릭하여 연결을 시작합니다
2. 처음 연결하는 경우 보안 경고가 표시됩니다 - **Yes**를 클릭하여 서버를 신뢰합니다
3. 메시지가 표시되면 사용자 이름을 입력합니다
4. 메시지가 표시되면 비밀번호를 입력합니다

![PuTTY 연결 완료](/images/guides/ssh-tunnel/sshtunnel_3.webp)

연결되면 브라우저를 열고 `http://127.0.0.1:7657`로 이동하여 원격 I2P 콘솔에 액세스할 수 있습니다

### 단계 1: PuTTY 다운로드 및 설치

매번 재구성하는 것을 피하려면:

1. **Session** 카테고리로 돌아갑니다
2. **Saved Sessions**에 이름을 입력합니다 (예: "I2P Tunnel")
3. **Save**를 클릭합니다
4. 다음번에는 이 세션을 불러오고 **Open**을 클릭하기만 하면 됩니다

## Creating SSH Tunnels on Linux

Linux 시스템은 터미널에 SSH가 내장되어 있어 tunnel 생성이 빠르고 간단합니다.

### 2단계: SSH 연결 구성

터미널을 열고 SSH 터널 명령을 실행하세요:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**교체**: - `7657` (첫 번째 항목): 원하는 로컬 포트 - `127.0.0.1:7657`: 원격 서버의 대상 주소 및 포트 - `i2p`: 원격 서버의 사용자 이름 - `20.228.143.58`: 원격 서버의 IP 주소

![Linux SSH 터널 생성](/images/guides/ssh-tunnel/sshtunnel_4.webp)

메시지가 표시되면 비밀번호를 입력하세요. 연결되면 터널이 활성화됩니다.

브라우저에서 `http://127.0.0.1:7657`로 원격 I2P 콘솔에 접속하세요.

### 3단계: 터널 구성

터널은 SSH 세션이 실행되는 동안 활성 상태를 유지합니다. 백그라운드에서 계속 실행하려면:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**추가 플래그**: - `-f`: SSH를 백그라운드에서 실행 - `-N`: 원격 명령을 실행하지 않음 (터널만)

백그라운드 터널을 종료하려면 SSH 프로세스를 찾아서 종료하세요:

```bash
ps aux | grep ssh
kill [process_id]
```
### 4단계: 연결

더 나은 보안과 편의성을 위해 SSH 키 인증을 사용하세요:

1. SSH 키 페어 생성 (키 페어가 없는 경우):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. 공개 키를 원격 서버에 복사합니다:
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. 이제 비밀번호 없이 연결할 수 있습니다:
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Mac 시스템은 Linux와 동일한 SSH 클라이언트를 사용하므로 프로세스가 동일합니다.

### 선택사항: 세션 저장하기

터미널을 엽니다 (응용 프로그램 → 유틸리티 → 터미널). 그런 다음 다음을 실행합니다:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**교체**: - `7657` (첫 번째 항목): 원하는 로컬 포트 - `127.0.0.1:7657`: 원격 서버의 대상 주소 및 포트 - `i2p`: 원격 서버의 사용자 이름 - `20.228.143.58`: 원격 서버의 IP 주소

![Mac SSH 터널 생성](/images/guides/ssh-tunnel/sshtunnel_5.webp)

메시지가 표시되면 비밀번호를 입력하세요. 연결되면 `http://127.0.0.1:7657`에서 원격 I2P 콘솔에 접속할 수 있습니다

### Background Tunnels on Mac

Linux와 동일하게, 터널을 백그라운드에서 실행할 수 있습니다:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### 터미널 사용하기

Mac SSH 키 설정은 Linux와 동일합니다:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### 터널 활성 상태 유지

가장 일반적인 사용 사례 - 원격 I2P router 콘솔에 접속:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
그런 다음 브라우저에서 `http://127.0.0.1:7657`을 엽니다.

### SSH 키 사용 (권장)

여러 포트를 한 번에 포워딩:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
이것은 포트 7657 (I2P 콘솔)과 7658 (다른 서비스) 모두를 포워딩합니다.

### Custom Local Port

7657 포트가 이미 사용 중인 경우 다른 로컬 포트를 사용하세요:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
대신 `http://127.0.0.1:8080`에서 I2P 콘솔에 접속하세요.

## Troubleshooting

### 터미널 사용하기

**오류**: "bind: Address already in use"

**해결 방법**: 다른 로컬 포트를 선택하거나 해당 포트를 사용하는 프로세스를 종료하세요:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Mac에서의 백그라운드 터널

**오류**: "Connection refused" 또는 "channel 2: open failed"

**가능한 원인**: - 원격 서비스가 실행되지 않음 (원격 서버에서 I2P router가 실행 중인지 확인) - 방화벽이 연결을 차단함 - 잘못된 목적지 포트

**해결 방법**: 원격 서버에서 I2P router가 실행 중인지 확인하세요:

```bash
ssh user@remote-server "systemctl status i2p"
```
### Mac에서 SSH 키 설정

**오류**: "Permission denied" 또는 "Authentication failed"

**가능한 원인**: - 잘못된 사용자 이름 또는 비밀번호 - SSH 키가 올바르게 구성되지 않음 - 원격 서버에서 SSH 접근이 비활성화됨

**해결 방법**: 자격 증명을 확인하고 원격 서버에서 SSH 액세스가 활성화되어 있는지 확인하세요.

### Tunnel Drops Connection

**오류**: 일정 시간 비활성화 후 연결 끊김

**해결 방법**: SSH 설정 파일(`~/.ssh/config`)에 keep-alive 설정을 추가하세요:

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **SSH 키 사용**: 비밀번호보다 안전하며 침해가 어려움
- **비밀번호 인증 비활성화**: SSH 키 설정 후 서버에서 비밀번호 로그인 비활성화
- **강력한 비밀번호 사용**: 비밀번호 인증을 사용하는 경우 강력하고 고유한 비밀번호 사용
- **SSH 접근 제한**: 방화벽 규칙을 구성하여 신뢰할 수 있는 IP로 SSH 접근 제한
- **SSH 업데이트 유지**: SSH 클라이언트 및 서버 소프트웨어를 정기적으로 업데이트
- **로그 모니터링**: 서버의 SSH 로그에서 의심스러운 활동 확인
- **비표준 SSH 포트 사용**: 자동화된 공격을 줄이기 위해 기본 SSH 포트(22)를 변경

## Linux에서 SSH 터널 생성하기

### I2P 콘솔 접속하기

터널을 자동으로 설정하는 스크립트를 작성하세요:

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
실행 가능하게 만들기:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### 다중 터널

systemd 서비스를 생성하여 자동 터널 생성:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
추가:

```ini
[Unit]
Description=I2P SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L 7657:127.0.0.1:7657 i2p@20.228.143.58
Restart=always
RestartSec=10
User=your-username

[Install]
WantedBy=multi-user.target
```
활성화 및 시작:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### 커스텀 로컬 포트

동적 포워딩을 위한 SOCKS 프록시를 생성하세요:

```bash
ssh -D 8080 user@remote-server
```
브라우저를 `127.0.0.1:8080`을 SOCKS5 프록시로 사용하도록 설정하세요.

### Reverse Tunneling

원격 서버가 로컬 머신의 서비스에 접근할 수 있도록 허용:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### 포트가 이미 사용 중입니다

중간 서버를 통한 터널:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

SSH 터널링은 원격 I2P router 및 기타 서비스에 안전하게 접근하기 위한 강력한 도구입니다. Windows, Linux, Mac 중 무엇을 사용하든 프로세스는 간단하며 연결에 강력한 암호화를 제공합니다.

추가 도움이나 질문이 있으시면 I2P 커뮤니티를 방문하세요: - **포럼**: [i2pforum.net](https://i2pforum.net) - **IRC**: 다양한 네트워크의 #i2p - **문서**: [I2P Docs](/docs/)

---


*가이드는 원래 [Stormy Cloud](https://www.stormycloud.org)에서 작성되었으며, I2P 문서에 맞게 수정되었습니다.*
