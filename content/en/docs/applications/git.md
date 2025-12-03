---
title: "Git over I2P"
description: "Connecting Git clients to I2P-hosted services such as i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
aliases:
  - "/en/docs/applications/GIT.md"
  - /en/docs/applications/gitlab/
reviewStatus: "needs-review"
---

Cloning and pushing repositories inside I2P uses the same Git commands you already know—your client simply connects through I2P tunnels instead of TCP/IP. This guide walks through setting up an account, configuring tunnels, and dealing with slow links.

> **Quick start:** Read-only access works through the HTTP proxy: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Follow the steps below for SSH read/write access.

## 1. Create an Account

Choose an I2P Git service and register:

- Inside I2P: `http://git.idk.i2p`
- Clearnet mirror: `https://i2pgit.org`

Registration may require manual approval; check the landing page for instructions. Once approved, fork or create a repository so you have something to test with.

## 2. Configure an I2PTunnel Client (SSH)

1. Open the router console → **I2PTunnel** and add a new **Client** tunnel.
2. Enter the service’s destination (Base32 or Base64). For `git.idk.i2p` you’ll find both HTTP and SSH destinations on the project home page.
3. Choose a local port (for example `localhost:7442`).
4. Enable autostart if you plan to use the tunnel frequently.

The UI will confirm the new tunnel and show its status. When it is running, SSH clients can connect to `127.0.0.1` on the chosen port.

## 3. Clone via SSH

Use the tunnel port with `GIT_SSH_COMMAND` or an SSH config stanza:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```

If the first attempt fails (tunnels can be slow), try a shallow clone:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```

Configure Git to fetch all branches:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```

### Performance Tips

- Add one or two backup tunnels in the tunnel editor to improve resilience.
- For testing or low-risk repos you may reduce tunnel length to 1 hop, but be aware of the anonymity trade-off.
- Keep `GIT_SSH_COMMAND` in your environment or add an entry to `~/.ssh/config`:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```

Then clone using `git clone git@git.i2p:namespace/project.git`.

## 4. Workflow Suggestions

Adopt a fork-and-branch workflow common on GitLab/GitHub:

1. Set an upstream remote: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Keep your `master` in sync: `git pull upstream master`
3. Create feature branches for changes: `git checkout -b feature/new-thing`
4. Push branches to your fork: `git push origin feature/new-thing`
5. Submit a merge request, then fast-forward your fork’s master from upstream.

## 5. Privacy Reminders

- Git stores commit timestamps in your local timezone. To force UTC timestamps:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```

Use `git utccommit` instead of `git commit` when privacy matters.

- Avoid embedding clearnet URLs or IPs in commit messages or repository metadata if anonymity is a concern.

## 6. Troubleshooting

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

For advanced scenarios (mirroring external repos, seeding bundles), see the companion guides: [Git bundle workflows](/docs/applications/git-bundle/) and [Hosting GitLab over I2P](/docs/guides/gitlab/).
