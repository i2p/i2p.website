---
title: "I2P 상에서의 Gitlab 설정"
date: 2020-03-16
author: "idk"
description: "다른 사람들을 위해 I2P Git 저장소 미러 및 Clearnet(클리어넷) 저장소 브리지 제공"
categories: ["development"]
---

다음은 Docker로 서비스 자체를 관리하면서 Gitlab과 I2P를 구성할 때 사용하는 설정 절차입니다. 이 방식으로는 Gitlab을 I2P에서 매우 쉽게 호스팅할 수 있으며, 한 사람이 큰 어려움 없이 관리할 수 있습니다. 이 지침은 어떤 Debian 기반 시스템에서도 동작하고, Docker와 I2P router가 사용 가능한 모든 시스템으로도 손쉽게 이식할 수 있습니다.

## 의존성과 Docker

Gitlab은 컨테이너에서 실행되므로 메인 시스템에는 컨테이너에 필요한 의존성만 설치하면 됩니다. 편리하게도, 다음을 사용하여 필요한 모든 것을 설치할 수 있습니다:

```
sudo apt install docker.io
```
## Docker 컨테이너 가져오기

docker를 설치한 후에는 gitlab에 필요한 docker 컨테이너를 가져올 수 있습니다. *아직 실행하지 마십시오.*

```
docker pull gitlab/gitlab-ce
```
## Gitlab용 I2P HTTP 프록시 설정 (중요 정보, 선택 단계)

I2P 내부의 Gitlab 서버는 I2P 외부 인터넷의 서버와 상호작용할 수 있도록 하거나, 그렇게 하지 않도록 구성하여 운영할 수 있습니다. Gitlab 서버가 I2P 외부의 서버와 상호작용하는 것이 *허용되지 않는* 경우, I2P 외부 인터넷의 git 서버에서 git 저장소를 클론하는 방법으로는 해당 서버의 익명성이 해제되지 않습니다.

Gitlab 서버가 I2P 외부의 서버와 상호작용하는 것이 *허용*되는 경우, 이는 사용자를 위한 "Bridge"(브리지) 역할을 할 수 있어 I2P 외부의 콘텐츠를 I2P에서 접근 가능한 소스로 미러링하는 데 사용할 수 있지만, 이 경우에는 *익명적이지 않습니다*.

**웹 리포지토리에 접근할 수 있는 브리지된 비익명 Gitlab 인스턴스를 원한다면**, 추가 수정은 필요하지 않습니다.

**웹 전용 저장소(Web-Only Repositories)에 접근할 수 없는 I2P 전용 Gitlab 인스턴스를 원한다면**, Gitlab이 I2P HTTP 프록시를 사용하도록 구성해야 합니다. 기본 I2P HTTP 프록시는 `127.0.0.1`에서만 수신하므로, Docker 네트워크의 호스트/게이트웨이 주소(보통 `172.17.0.1`)에서 수신하도록 Docker용 새 프록시를 설정해야 합니다. 저는 포트 `4446`으로 설정합니다.

## 로컬에서 컨테이너 시작하기

설정을 완료하면 컨테이너를 시작하고 Gitlab 인스턴스를 로컬에서 공개할 수 있습니다:

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
Visit your Local Gitlab instance and set up your admin account. Choose a strong password, and configure user account limits to match your resources.

## 서비스 tunnel을 설정하고 호스트명을 등록하세요

로컬에 Gitlab을 설정했으면 I2P Router console로 이동하십시오. 서버 tunnel을 두 개 설정해야 합니다. 하나는 TCP 포트 8080의 Gitlab 웹(HTTP) 인터페이스로, 다른 하나는 TCP 포트 8022의 Gitlab SSH 인터페이스로 연결되도록 설정하십시오.

### Gitlab Web(HTTP) Interface

웹 인터페이스에는 "HTTP" server tunnel을 사용하세요. http://127.0.0.1:7657/i2ptunnelmgr 에서 "New Tunnel Wizard"를 실행하고 다음 값을 입력하세요:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

SSH 인터페이스의 경우 "Standard" 서버 tunnel을 사용하세요. http://127.0.0.1:7657/i2ptunnelmgr 에서 "New Tunnel Wizard"를 실행하고 다음 값을 입력하세요:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

마지막으로, `gitlab.rb`를 수정했거나 호스트 이름을 등록한 경우, 설정이 적용되도록 gitlab 서비스를 다시 시작해야 합니다.
