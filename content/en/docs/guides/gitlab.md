---
title: "Running GitLab over I2P"
description: "Deploying GitLab inside I2P using Docker and an I2P router"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

Hosting GitLab inside I2P is straightforward: run the GitLab omnibus container, expose it on loopback, and forward traffic through an I2P tunnel. The steps below mirror the configuration used for `git.idk.i2p` but work for any self-hosted instance.

## 1. Prerequisites

- Debian or another Linux distribution with Docker Engine installed (`sudo apt install docker.io` or `docker-ce` from Docker’s repo).
- An I2P router (Java I2P or i2pd) with enough bandwidth to serve your users.
- Optional: a dedicated VM so GitLab and the router stay isolated from your desktop environment.

## 2. Pull the GitLab Image

```bash
docker pull gitlab/gitlab-ce:latest
```

The official image is built from Ubuntu base layers and updated regularly. Audit the [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) if you need additional reassurance.

## 3. Decide on Bridging vs. I2P-Only

- **I2P-only** instances never contact clearnet hosts. Users may mirror repositories from other I2P services but not from GitHub/GitLab.com. This maximises anonymity.
- **Bridged** instances reach out to clearnet Git hosts via an HTTP proxy. This is useful for mirroring public projects into I2P but it deanonymises the server’s outbound requests.

If you choose the bridged mode, configure GitLab to use an I2P HTTP proxy bound on the Docker host (for example `http://172.17.0.1:4446`). The default router proxy listens on `127.0.0.1` only; add a new proxy tunnel bound to the Docker gateway address.

## 4. Start the Container

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

- Bind the published ports to loopback; the I2P tunnels will expose them as needed.
- Replace `/srv/gitlab/...` with storage paths that suit your host.

Once the container is running, visit `https://127.0.0.1:8443/`, set an admin password, and configure account limits.

## 5. Expose GitLab Through I2P

Create three I2PTunnel **server** tunnels:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |

Configure each tunnel with appropriate tunnel lengths and bandwidth. For public instances, 3 hops with 4–6 tunnels per direction is a good starting point. Publish the resulting Base32/Base64 destinations on your landing page so users can configure client tunnels.

### Destination Enforcement

If you use HTTP(S) tunnels, enable destination enforcement so only the intended hostname can reach the service. This prevents the tunnel from being abused as a generic proxy.

## 6. Maintenance Tips

- Run `docker exec gitlab gitlab-ctl reconfigure` whenever you change GitLab settings.
- Monitor disk usage (`/srv/gitlab/data`)—Git repositories grow quickly.
- Back up configuration and data directories regularly. GitLab’s [backup rake tasks](https://docs.gitlab.com/ee/raketasks/backup_restore.html) work inside the container.
- Consider placing an external monitoring tunnel in client mode to ensure the service is reachable from the broader network.

## 7. Related Guides

- [Embedding I2P in your application](/docs/applications/embedding/)
- [Git over I2P (client guide)](/docs/applications/git/)
- [Git bundles for offline/slow networks](/docs/applications/git-bundle/)

A well-configured GitLab instance provides a collaborative development hub wholly inside I2P. Keep the router healthy, stay current with GitLab security updates, and coordinate with the community as your user base grows.
