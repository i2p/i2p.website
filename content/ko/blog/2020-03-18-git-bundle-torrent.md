---
title: "Git 번들로 I2P 소스 코드 가져오기"
date: 2020-03-18
author: "idk"
description: "I2P 소스 코드를 비트토렌트를 통해 다운로드하십시오"
categories: ["development"]
---

I2P를 통해 대규모 소프트웨어 저장소를 복제하는 일은 어렵고, git을 사용하면 때로는 이를 더 어렵게 만들기도 합니다. 다행히, 경우에 따라 git이 이를 더 쉽게 만들어 주기도 합니다. Git에는 `git bundle` 명령이 있으며, 이를 사용하면 Git 저장소를 하나의 파일로 변환할 수 있고, 그렇게 만든 파일을 로컬 디스크의 위치에서 git이 clone(복제), fetch(가져오기), import(임포트)할 수 있습니다. 이 기능을 BitTorrent 다운로드와 결합하면, `git clone`과 관련된 남은 문제들을 해결할 수 있습니다.

## 시작하기 전에

git 번들을 생성하려는 경우, mtn 저장소가 아니라 **git** 저장소의 전체 사본을 이미 **반드시** 보유하고 있어야 합니다. github 또는 git.idk.i2p에서 가져올 수 있지만, 얕은 클론(--depth=1로 수행한 클론)은 *작동하지 않습니다*. 겉보기에는 번들을 만든 것처럼 보이도록 조용히 실패하지만, 그것으로 클론을 시도하면 실패합니다. 미리 생성된 git 번들을 가져오기만 하는 경우라면, 이 섹션은 적용되지 않습니다.

## 비트토렌트를 통해 I2P 소스 코드 가져오기

누군가가 미리 당신을 위해 생성해 둔 기존 `git bundle`에 해당하는 토렌트 파일 또는 마그넷 링크를 제공해 주어야 합니다. BitTorrent로 번들을 받으면, 그 번들로부터 작업용 저장소를 만들기 위해 git을 사용해야 합니다.

## `git clone` 사용하기

git 번들에서 복제하는 것은 쉽습니다. 방법은 다음과 같습니다:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
다음과 같은 오류가 발생하는 경우, 대신 수동으로 git init 및 git fetch를 사용해 보십시오:

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## `git init` 및 `git fetch` 사용

먼저, git 저장소로 전환할 i2p.i2p 디렉터리를 만듭니다:

```
mkdir i2p.i2p && cd i2p.i2p
```
다음으로, 변경 사항을 다시 이 저장소로 가져올 수 있도록 빈 git 저장소를 초기화합니다:

```
git init
```
마지막으로, 번들에서 저장소를 가져옵니다:

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## 번들 원격 저장소를 업스트림 원격 저장소로 교체

이제 번들을 확보했으므로, 원격을 업스트림 저장소 소스로 설정해 변경 사항을 최신 상태로 유지할 수 있습니다:

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## 번들 생성

먼저, 사용자용 Git 가이드를 따라 i2p.i2p 저장소의 `--unshallow`를 성공적으로 적용한 클론을 얻을 때까지 따르십시오. 이미 클론이 있다면, 토렌트 번들을 생성하기 전에 반드시 `git fetch --unshallow`를 실행하십시오.

그것을 갖추었으면, 간단히 해당하는 ant 타깃을 실행하면 됩니다:

```
ant bundle
```
그리고 생성된 번들을 I2PSnark 다운로드 디렉터리에 복사하십시오. 예를 들어:

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
한두 분 내에 I2PSnark가 토렌트를 감지합니다. 토렌트 시딩을 시작하려면 "Start" 버튼을 클릭하세요.
