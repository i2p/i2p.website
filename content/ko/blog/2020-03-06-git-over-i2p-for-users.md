---
title: "사용자를 위한 I2P를 통한 Git"
date: 2020-03-06
author: "idk"
description: "I2P를 통한 Git"
categories: ["development"]
---

I2P Tunnel을 통해 git 접근을 설정하는 튜토리얼입니다. 이 tunnel은 I2P에서 단일 git 서비스에 접근하기 위한 접속 지점 역할을 합니다. 이는 I2P를 monotone에서 Git으로 전환하려는 전반적인 노력의 일부입니다.

## 무엇보다 먼저: 서비스가 공개적으로 제공하는 기능을 숙지하라

git 서비스가 어떻게 구성되어 있는지에 따라 모든 서비스를 동일한 주소에서 제공할 수도 있고 그렇지 않을 수도 있습니다. git.idk.i2p의 경우 공개 HTTP URL과 사용자의 Git SSH 클라이언트에 설정할 SSH URL이 있습니다. 둘 중 어느 것을 사용해도 push 또는 pull을 할 수 있지만, SSH를 권장합니다.

## 먼저: Git 서비스에서 계정을 생성하세요

원격 git 서비스에 저장소를 만들려면 해당 서비스에 사용자 계정으로 가입하세요. 물론 로컬에서 저장소를 생성하고 이를 원격 git 서비스로 푸시하는 것도 가능하지만, 대부분의 경우 계정이 필요하며 서버에서 저장소를 위한 공간을 미리 만들어 두어야 합니다.

## 둘째: 테스트용 프로젝트 만들기

설정 과정이 제대로 작동하는지 확인하려면, 서버에서 테스트할 수 있도록 저장소를 하나 만들어 두는 것이 도움이 됩니다. i2p-hackers/i2p.i2p 저장소로 이동하여 자신의 계정으로 포크하십시오.

## 셋째: git 클라이언트 tunnel을 설정하세요

서버에 읽기/쓰기 액세스가 필요하다면 SSH 클라이언트를 위한 tunnel을 설정해야 합니다. 읽기 전용 HTTP/S 복제만 필요하다면, 이 모든 과정을 건너뛰고 http_proxy 환경 변수를 사용하여 git이 사전 구성된 I2P HTTP Proxy를 사용하도록 설정하면 됩니다. 예:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
SSH 접속을 위해 http://127.0.0.1:7657/i2ptunnelmgr에서 "New Tunnel Wizard"를 실행하고 Git 서비스의 SSH base32 주소를 가리키도록 client tunnel을 설정하십시오.

## 네 번째: 복제 시도하기

이제 tunnel 설정이 모두 완료되었으니, SSH를 통해 클론을 시도할 수 있습니다:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
원격 측(remote end)이 예기치 않게 연결을 끊는 오류가 발생할 수 있습니다. 안타깝게도 git은 아직 resumable cloning(중단 후 재개 가능한 복제)을 지원하지 않습니다. 그때까지는 이 문제를 처리하는 비교적 쉬운 방법이 몇 가지 있습니다. 첫 번째이자 가장 쉬운 방법은 얕은 깊이로 복제해 보는 것입니다:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
얕은 클론을 수행한 후, 저장소 디렉터리로 이동하여 다음을 실행하면 나머지를 재개 가능한 방식으로 가져올 수 있습니다:

```
git fetch --unshallow
```
이 시점에서는 아직 모든 브랜치를 가지고 있지 않습니다. 다음을 실행하면 가져올 수 있습니다:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## 개발자를 위한 권장 워크플로우

버전 관리는 제대로 사용할 때 가장 효과적입니다! 우리는 fork-first(포크 우선), feature-branch(기능 브랜치) 워크플로우를 강력히 권장합니다:

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```