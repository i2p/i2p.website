---
title: "Git 번들 (I2P용)"
description: "```
git bundle과 BitTorrent를 사용하여 대용량 저장소 가져오기 및 배포하기
```"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

네트워크 상황으로 인해 `git clone`이 불안정할 때, BitTorrent나 다른 파일 전송 방식을 통해 저장소를 **git bundle**로 배포할 수 있습니다. bundle은 전체 저장소 히스토리를 포함하는 단일 파일입니다. 다운로드 후에는 로컬에서 fetch하고 나서 다시 업스트림 리모트로 전환하면 됩니다.

## 1. 시작하기 전에

번들을 생성하려면 **완전한** Git 클론이 필요합니다. `--depth 1`로 생성된 얕은 클론은 정상적으로 작동하는 것처럼 보이지만 다른 사람이 사용하려고 할 때 실패하는 손상된 번들을 조용히 생성합니다. 항상 신뢰할 수 있는 소스(GitHub의 [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), I2P Gitea 인스턴스인 [i2pgit.org](https://i2pgit.org), 또는 I2P를 통한 `git.idk.i2p`)에서 가져오고, 필요한 경우 `git fetch --unshallow`를 실행하여 번들을 생성하기 전에 얕은 클론을 전체 클론으로 변환하세요.

기존 번들을 사용하기만 하는 경우, 그냥 다운로드하면 됩니다. 특별한 준비는 필요하지 않습니다.

## 2. 번들 다운로드

### Obtaining the Bundle File

I2PSnark(I2P에 내장된 토렌트 클라이언트) 또는 I2P 플러그인이 설치된 BiglyBT와 같은 다른 I2P 호환 클라이언트를 사용하여 BitTorrent를 통해 번들 파일을 다운로드하세요.

**중요**: I2PSnark는 I2P 네트워크 전용으로 생성된 토렌트에서만 작동합니다. 일반 클리어넷 토렌트는 호환되지 않는데, I2P는 IP 주소와 포트 대신 Destination(387바이트 이상의 주소)을 사용하기 때문입니다.

번들 파일 위치는 I2P 설치 유형에 따라 다릅니다:

- **사용자/수동 설치** (Java 설치 프로그램으로 설치): `~/.i2p/i2psnark/`
- **시스템/데몬 설치** (apt-get 또는 패키지 관리자로 설치): `/var/lib/i2p/i2p-config/i2psnark/`

BiglyBT 사용자는 구성된 다운로드 디렉토리에서 다운로드한 파일을 찾을 수 있습니다.

### Cloning from the Bundle

**표준 방법** (대부분의 경우 작동함):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
`fatal: multiple updates for ref` 오류가 발생하는 경우 (Git 2.21.0 이상 버전에서 전역 Git 설정에 충돌하는 fetch refspec이 포함되어 있을 때 발생하는 알려진 문제), 수동 초기화 방법을 사용하세요:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
또는 `--update-head-ok` 플래그를 사용할 수 있습니다:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### 번들 파일 획득하기

번들에서 클론한 후, 향후 fetch가 I2P 또는 clearnet을 통해 이루어지도록 클론이 실제 원격 저장소를 가리키도록 설정하세요:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
또는 일반 인터넷(clearnet) 접속의 경우:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
I2P SSH 접속을 위해서는 I2P 라우터 콘솔에서 SSH 클라이언트 tunnel을 설정해야 합니다(일반적으로 포트 7670). 이 tunnel은 `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`를 가리켜야 합니다. 비표준 포트를 사용하는 경우:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### 번들에서 복제하기

저장소가 **완전한 복제본**(shallow가 아닌)으로 완전히 최신 상태인지 확인하세요:

```bash
git fetch --all
```
shallow clone이 있는 경우, 먼저 변환하세요:

```bash
git fetch --unshallow
```
### 라이브 리모트로 전환하기

**Ant 빌드 타겟 사용** (I2P 소스 트리에 권장):

```bash
ant git-bundle
```
이는 `i2p.i2p.bundle` (번들 파일)과 `i2p.i2p.bundle.torrent` (BitTorrent 메타데이터)를 모두 생성합니다.

**git bundle을 직접 사용하기**:

```bash
git bundle create i2p.i2p.bundle --all
```
더 선택적인 번들의 경우:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

배포하기 전에 항상 번들을 검증하세요:

```bash
git bundle verify i2p.i2p.bundle
```
이는 번들이 유효함을 확인하고 필요한 선행 커밋을 표시합니다.

### 사전 요구사항

번들과 토렌트 메타데이터를 I2PSnark 디렉토리에 복사하세요:

**사용자 설치의 경우**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**시스템 설치의 경우**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark는 .torrent 파일을 수 초 내에 자동으로 감지하고 로드합니다. [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark)에서 웹 인터페이스에 접속하여 시딩을 시작하세요.

## 4. Creating Incremental Bundles

주기적인 업데이트를 위해서는 마지막 번들 이후의 새로운 커밋만 포함하는 증분 번들을 생성하세요:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
사용자가 이미 base 저장소를 가지고 있다면 incremental 번들에서 가져올 수 있습니다:

```bash
git fetch /path/to/update.bundle
```
증분 번들이 예상되는 사전 요구 커밋을 표시하는지 항상 확인하십시오:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

번들에서 작동하는 저장소를 확보했다면, 다른 Git 클론처럼 다루면 됩니다:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
또는 더 간단한 워크플로우의 경우:

```bash
git fetch origin
git pull origin master
```
## 3. 번들 생성하기

- **탄력적인 배포**: 대규모 저장소는 BitTorrent를 통해 공유될 수 있으며, 재시도, 조각 검증, 재개가 자동으로 처리됩니다.
- **Peer-to-peer 부트스트랩**: 새로운 기여자는 I2P 네트워크의 인근 peer로부터 클론을 부트스트랩한 다음, Git 호스트에서 직접 증분 변경사항을 가져올 수 있습니다.
- **서버 부하 감소**: Mirror는 주기적인 번들을 게시하여 활성 Git 호스트의 부담을 줄일 수 있으며, 이는 대규모 저장소나 느린 네트워크 환경에서 특히 유용합니다.
- **오프라인 전송**: 번들은 BitTorrent뿐만 아니라 모든 파일 전송 수단(USB 드라이브, 직접 전송, sneakernet)에서 작동합니다.

번들은 라이브 원격 저장소를 대체하지 않습니다. 단지 초기 클론이나 주요 업데이트를 위한 더 탄력적인 부트스트래핑 방법을 제공할 뿐입니다.

## 7. Troubleshooting

### 번들 생성하기

**문제**: 번들 생성은 성공하지만 다른 사용자가 번들에서 클론할 수 없습니다.

**원인**: 소스 클론이 shallow(얕은 클론)입니다(`--depth` 옵션으로 생성됨).

**해결 방법**: 번들을 생성하기 전에 전체 복제본으로 변환하세요:

```bash
git fetch --unshallow
```
### 번들 검증하기

**문제**: 번들에서 클론할 때 `fatal: multiple updates for ref` 오류 발생.

**원인**: Git 2.21.0 이상 버전이 `~/.gitconfig`의 전역 fetch refspec과 충돌합니다.

**해결 방법**: 1. 수동 초기화 사용: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. `--update-head-ok` 플래그 사용: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. 충돌하는 설정 제거: `git config --global --unset remote.origin.fetch`

### I2PSnark를 통한 배포

**문제**: `git bundle verify`가 누락된 전제 조건을 보고합니다.

**원인**: 증분 번들 또는 불완전한 소스 복제.

**해결 방법**: 필수 커밋을 먼저 가져오거나, 기본 번들을 먼저 사용한 다음 증분 업데이트를 적용하세요.
