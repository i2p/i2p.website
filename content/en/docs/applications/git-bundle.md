---
title: "Git Bundles for I2P"
description: "Fetching and distributing large repositories with git bundle and BitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

When network conditions make `git clone` unreliable, you can distribute repositories as **git bundles** over BitTorrent or any other file transport. A bundle is a single file containing the entire repository history. Once downloaded, you fetch from it locally and then switch back to the upstream remote.

## 1. Before You Start

Generating a bundle requires a **complete** Git clone. Shallow clones created with `--depth 1` will silently produce broken bundles that appear to work but fail when others try to use them. Always fetch from a trusted source (GitHub at [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), the I2P Gitea instance at [i2pgit.org](https://i2pgit.org), or `git.idk.i2p` over I2P) and run `git fetch --unshallow` if necessary to convert any shallow clone to a full clone before creating bundles.

If you are only consuming an existing bundle, just download it. No special preparation required.

## 2. Downloading a Bundle

### Obtaining the Bundle File

Download the bundle file via BitTorrent using I2PSnark (the built-in torrent client in I2P) or other I2P-compatible clients like BiglyBT with the I2P plugin. 

**Important**: I2PSnark only works with torrents specifically created for the I2P network. Standard clearnet torrents are not compatible because I2P uses Destinations (387+ byte addresses) instead of IP addresses and ports.

The bundle file location depends on your I2P installation type:

- **User/manual installations** (installed with Java installer): `~/.i2p/i2psnark/`
- **System/daemon installations** (installed via apt-get or package manager): `/var/lib/i2p/i2p-config/i2psnark/`

BiglyBT users will find downloaded files in their configured downloads directory.

### Cloning from the Bundle

**Standard method** (works in most cases):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```

If you encounter `fatal: multiple updates for ref` errors (a known issue in Git 2.21.0 and later when global Git config contains conflicting fetch refspecs), use the manual initialization approach:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```

Alternatively, you can use the `--update-head-ok` flag:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```

### Switching to the Live Remote

After cloning from the bundle, point your clone at the live remote so future fetches go over I2P or clearnet:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```

Or for clearnet access:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```

For I2P SSH access, you need an SSH client tunnel configured in your I2P router console (typically port 7670) pointing to `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`. If using a non-standard port:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```

## 3. Creating a Bundle

### Prerequisites

Ensure your repository is fully up to date with a **complete clone** (not shallow):

```bash
git fetch --all
```

If you have a shallow clone, convert it first:

```bash
git fetch --unshallow
```

### Generating the Bundle

**Using the Ant build target** (recommended for I2P source tree):

```bash
ant git-bundle
```

This creates both `i2p.i2p.bundle` (the bundle file) and `i2p.i2p.bundle.torrent` (BitTorrent metadata).

**Using git bundle directly**:

```bash
git bundle create i2p.i2p.bundle --all
```

For more selective bundles:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```

### Verifying Your Bundle

Always verify the bundle before distributing:

```bash
git bundle verify i2p.i2p.bundle
```

This confirms the bundle is valid and shows any prerequisite commits required.

### Distributing via I2PSnark

Copy the bundle and its torrent metadata into your I2PSnark directory:

**For user installations**:
```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```

**For system installations**:
```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```

I2PSnark automatically detects and loads .torrent files within seconds. Access the web interface at [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) to start seeding.

## 4. Creating Incremental Bundles

For periodic updates, create incremental bundles containing only new commits since the last bundle:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```

Users can fetch from the incremental bundle if they already have the base repository:

```bash
git fetch /path/to/update.bundle
```

Always verify incremental bundles show the expected prerequisite commits:

```bash
git bundle verify update.bundle
```

## 5. Updating After the Initial Clone

Once you have a working repository from the bundle, treat it like any other Git clone:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```

Or for simpler workflows:

```bash
git fetch origin
git pull origin master
```

## 6. Why Bundles Help

- **Resilient distribution**: Large repositories can be shared over BitTorrent, which handles retries, piece verification, and resume automatically.
- **Peer-to-peer bootstrap**: New contributors can bootstrap their clone from nearby peers on the I2P network, then fetch incremental changes directly from Git hosts.
- **Reduced server load**: Mirrors can publish periodic bundles to relieve pressure on live Git hosts, especially useful for large repositories or slow network conditions.
- **Offline transport**: Bundles work on any file transport (USB drives, direct transfers, sneakernet), not just BitTorrent.

Bundles do not replace live remotes. They simply provide a more resilient bootstrapping method for initial clones or major updates.

## 7. Troubleshooting

### Shallow Clone Issues

**Problem**: Bundle creation succeeds but others cannot clone from the bundle.

**Cause**: Your source clone is shallow (created with `--depth`).

**Solution**: Convert to full clone before creating bundles:
```bash
git fetch --unshallow
```

### Multiple Updates for Ref Error

**Problem**: `fatal: multiple updates for ref` when cloning from bundle.

**Cause**: Git 2.21.0+ conflicts with global fetch refspecs in `~/.gitconfig`.

**Solutions**:
1. Use manual initialization: `mkdir repo && cd repo && git init && git fetch /path/to/bundle`
2. Use `--update-head-ok` flag: `git fetch --update-head-ok /path/to/bundle '*:*'`
3. Remove conflicting config: `git config --global --unset remote.origin.fetch`

### Bundle Verification Fails

**Problem**: `git bundle verify` reports missing prerequisites.

**Cause**: Incremental bundle or incomplete source clone.

**Solution**: Either fetch prerequisite commits or use the base bundle first, then apply incremental updates.

## Additional Resources

For comprehensive Git over I2P setup, SSH tunnel configuration, and hosting your own repositories, see the [Git over I2P guide](https://geti2p.net/en/docs/applications/git/) at the official I2P documentation site.

For I2P installation and setup, visit [geti2p.net](https://geti2p.net).
