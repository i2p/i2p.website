---
title: "Gitlab over I2P Setup"
date: 2020-03-16
author: "idk"
description: "Mirror I2P Git repositories and Bridge Clearnet repositories for others"
categories: ["development"]
---

This is the setup process I use for configuring Gitlab and I2P, with Docker in place to manage the service itself. Gitlab is very easy to host on I2P in this fashion, it can be administered by one person without much difficulty. These instructions should work on any Debian-based system and should easily translate to any system where Docker and an I2P router are available.

## Dependencies and Docker

Because Gitlab runs in a container, we only need to install the dependencies required for the container on our main system. Conveniently, you can install everything you need with:

```
sudo apt install docker.io
```
## Fetch the Docker Containers

Once you have docker installed, you can fetch the docker containers required for gitlab. *Don't run them yet.*

```
docker pull gitlab/gitlab-ce
```
## Set up an I2P HTTP Proxy for Gitlab (Important information, optional steps)

Gitlab servers inside of I2P can be run with or without the ability to interact with servers on the internet outside of I2P. In the case where the Gitlab server is *not allowed* to interact with servers outside of I2P, they cannot be de-anonymized by cloning a git repository from a git server on the internet outside of I2P.

In the case where the Gitlab server is *allowed* to interact with servers outside of I2P, it can act as a "Bridge" for the users, who can use it to mirror content outside I2P to an I2P-accessible source, however it *is not anonymous* in this case.

**If you want to have a bridged, non-anonymous Gitlab instance with access to web repositories**, no further modification is necessary.

**If you want to have an I2P-Only Gitlab instance with no access to Web-Only Repositories**, you will need to configure Gitlab to use an I2P HTTP Proxy. Since the default I2P HTTP proxy only listens on `127.0.0.1`, you will need to set up a new one for Docker that listens on the Host/Gateway address of the Docker network, which is usually `172.17.0.1`. I configure mine on port `4446`.

## Start the Container Locally

Once you have that set up, you can start the container and publish your Gitlab instance locally:

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

## Set up your Service tunnels and sign up for a Hostname

Once you have Gitlab set up locally, go to the I2P Router console. You will need to set up two server tunnels, one leading to the Gitlab web(HTTP) interface on TCP port 8080, and one to the Gitlab SSH interface on TCP Port 8022.

### Gitlab Web(HTTP) Interface

For the Web interface, use an "HTTP" server tunnel. From http://127.0.0.1:7657/i2ptunnelmgr launch the "New Tunnel Wizard" and enter the following values:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

For the SSH interface, use a "Standard" server tunnel. From http://127.0.0.1:7657/i2ptunnelmgr launch the "New Tunnel Wizard" and enter the following values:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Finally, if you either modified `gitlab.rb` or you registered a hostname, you will need to re-start the gitlab service for the settings to take effect.
