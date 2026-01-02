---
title: "I2P를 통한 GitLab 실행"
description: "Docker와 I2P router를 사용하여 I2P 내부에 GitLab 배포하기"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

I2P 내부에서 GitLab을 호스팅하는 것은 간단합니다: GitLab omnibus 컨테이너를 실행하고, 루프백에 노출시킨 다음, I2P tunnel을 통해 트래픽을 포워딩하면 됩니다. 아래 단계는 `git.idk.i2p`에 사용된 구성을 반영하지만 모든 자체 호스팅 인스턴스에서 작동합니다.

## 1. 전제 조건

- Docker Engine이 설치된 Debian 또는 다른 Linux 배포판 (`sudo apt install docker.io` 또는 Docker 저장소의 `docker-ce`).
- 사용자에게 서비스를 제공하기에 충분한 대역폭을 가진 I2P router (Java I2P 또는 i2pd).
- 선택사항: GitLab과 router를 데스크톱 환경에서 격리하기 위한 전용 VM.

## 2. GitLab 이미지 가져오기

```bash
docker pull gitlab/gitlab-ce:latest
```
공식 이미지는 Ubuntu 기본 레이어에서 빌드되며 정기적으로 업데이트됩니다. 추가적인 확신이 필요하다면 [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile)을 검토하세요.

## 3. 브리지 모드 vs. I2P 전용 모드 결정

- **I2P 전용** 인스턴스는 클리어넷 호스트에 절대 접속하지 않습니다. 사용자는 다른 I2P 서비스에서 저장소를 미러링할 수 있지만 GitHub/GitLab.com에서는 할 수 없습니다. 이는 익명성을 최대화합니다.
- **브리지** 인스턴스는 HTTP 프록시를 통해 클리어넷 Git 호스트에 접속합니다. 이는 공개 프로젝트를 I2P로 미러링하는 데 유용하지만 서버의 아웃바운드 요청을 비익명화합니다.

브리지 모드를 선택한 경우, Docker 호스트에 바인딩된 I2P HTTP 프록시(예: `http://172.17.0.1:4446`)를 사용하도록 GitLab을 구성하세요. 기본 라우터 프록시는 `127.0.0.1`에서만 수신 대기합니다. Docker 게이트웨이 주소에 바인딩된 새 프록시 tunnel을 추가하세요.

## 4. 컨테이너 시작

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- 게시된 포트를 루프백에 바인딩하세요. I2P tunnel이 필요에 따라 노출합니다.
- `/srv/gitlab/...`을 호스트에 맞는 저장소 경로로 교체하세요.

컨테이너가 실행되면 `https://127.0.0.1:8443/`를 방문하여 관리자 비밀번호를 설정하고 계정 제한을 구성하세요.

## 5. I2P를 통한 GitLab 노출

세 개의 I2PTunnel **서버** 터널을 생성하세요:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
각 tunnel을 적절한 tunnel 길이와 대역폭으로 구성하십시오. 공개 인스턴스의 경우, 방향당 4–6개의 tunnel로 3홉을 설정하는 것이 좋은 출발점입니다. 사용자가 클라이언트 tunnel을 구성할 수 있도록 결과로 생성된 Base32/Base64 destination을 랜딩 페이지에 게시하십시오.

### Destination Enforcement

HTTP(S) 터널을 사용하는 경우, destination enforcement를 활성화하여 의도된 호스트명만 서비스에 접근할 수 있도록 하십시오. 이는 터널이 일반 프록시로 악용되는 것을 방지합니다.

## 6. Maintenance Tips

- GitLab 설정을 변경할 때마다 `docker exec gitlab gitlab-ctl reconfigure`를 실행하세요.
- 디스크 사용량(`/srv/gitlab/data`)을 모니터링하세요—Git 저장소는 빠르게 증가합니다.
- 설정 및 데이터 디렉토리를 정기적으로 백업하세요. GitLab의 [백업 rake 작업](https://docs.gitlab.com/ee/raketasks/backup_restore.html)은 컨테이너 내부에서 작동합니다.
- 외부 모니터링 tunnel을 클라이언트 모드로 배치하여 더 넓은 네트워크에서 서비스에 접근할 수 있는지 확인하는 것을 고려하세요.

## 6. 유지보수 팁

- [애플리케이션에 I2P 임베딩하기](/docs/applications/embedding/)
- [I2P를 통한 Git (클라이언트 가이드)](/docs/applications/git/)
- [오프라인/느린 네트워크를 위한 Git 번들](/docs/applications/git-bundle/)

잘 구성된 GitLab 인스턴스는 I2P 내부에서 완전히 작동하는 협업 개발 허브를 제공합니다. router를 건강하게 유지하고, GitLab 보안 업데이트를 최신 상태로 유지하며, 사용자 기반이 성장함에 따라 커뮤니티와 협력하세요.
