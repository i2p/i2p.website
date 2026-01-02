---
title: "I2P를 통한 Git"
description: "i2pgit.org와 같은 I2P 호스팅 서비스에 Git 클라이언트 연결하기"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

I2P 내에서 저장소를 복제하고 푸시하는 것은 이미 알고 있는 Git 명령어를 그대로 사용합니다. 클라이언트가 TCP/IP 대신 I2P tunnel을 통해 연결할 뿐입니다. 이 가이드는 계정 설정, tunnel 구성, 그리고 느린 연결 처리 방법을 안내합니다.

> **빠른 시작:** 읽기 전용 접근은 HTTP 프록시를 통해 작동합니다: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. SSH 읽기/쓰기 접근을 위해서는 아래 단계를 따르세요.

## 1. 계정 만들기

I2P Git 서비스를 선택하고 등록하세요:

- I2P 내부: `http://git.idk.i2p`
- Clearnet 미러: `https://i2pgit.org`

등록에는 수동 승인이 필요할 수 있습니다. 안내 페이지에서 지침을 확인하세요. 승인되면 저장소를 포크하거나 생성하여 테스트할 수 있는 환경을 준비하세요.

## 2. I2PTunnel 클라이언트 구성 (SSH)

1. router console → **I2PTunnel**을 열고 새로운 **Client** 터널을 추가합니다.
2. 서비스의 destination(Base32 또는 Base64)을 입력합니다. `git.idk.i2p`의 경우 프로젝트 홈페이지에서 HTTP와 SSH destination을 모두 찾을 수 있습니다.
3. 로컬 포트를 선택합니다(예: `localhost:7442`).
4. 터널을 자주 사용할 계획이라면 자동 시작을 활성화합니다.

UI가 새 터널을 확인하고 상태를 표시합니다. 실행 중일 때, SSH 클라이언트는 선택한 포트의 `127.0.0.1`에 연결할 수 있습니다.

## 3. SSH를 통한 클론

`GIT_SSH_COMMAND` 또는 SSH 설정 구문과 함께 터널 포트를 사용하세요:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
첫 번째 시도가 실패하면 (터널이 느릴 수 있음), shallow clone을 시도하세요:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
모든 브랜치를 가져오도록 Git 설정:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### 성능 최적화 팁

- 복원력을 향상시키기 위해 터널 편집기에서 백업 tunnel을 하나 또는 두 개 추가하세요.
- 테스트용이거나 위험도가 낮은 저장소의 경우 tunnel 길이를 1 hop으로 줄일 수 있지만, 익명성 트레이드오프를 유념하세요.
- 환경 변수에 `GIT_SSH_COMMAND`를 유지하거나 `~/.ssh/config`에 항목을 추가하세요:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
그런 다음 `git clone git@git.i2p:namespace/project.git`를 사용하여 클론합니다.

## 4. 워크플로우 제안

GitLab/GitHub에서 일반적으로 사용하는 fork-and-branch 워크플로우를 채택하세요:

1. upstream 원격 저장소 설정: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. `master` 브랜치를 동기화 상태로 유지: `git pull upstream master`
3. 변경사항을 위한 기능 브랜치 생성: `git checkout -b feature/new-thing`
4. 브랜치를 본인의 포크로 푸시: `git push origin feature/new-thing`
5. 병합 요청을 제출한 후, upstream에서 포크의 master를 fast-forward로 업데이트합니다.

## 5. 프라이버시 주의사항

- Git은 커밋 타임스탬프를 로컬 시간대로 저장합니다. UTC 타임스탬프를 강제 적용하려면:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
프라이버시가 중요할 때는 `git commit` 대신 `git utccommit`을 사용하세요.

- 익명성이 우려 사항인 경우 커밋 메시지나 저장소 메타데이터에 clearnet URL이나 IP를 포함하지 마세요.

## 6. 문제 해결

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
고급 시나리오(외부 저장소 미러링, 번들 시딩)에 대해서는 관련 가이드를 참조하세요: [Git 번들 워크플로우](/docs/applications/git-bundle/) 및 [I2P를 통한 GitLab 호스팅](/docs/guides/gitlab/).
