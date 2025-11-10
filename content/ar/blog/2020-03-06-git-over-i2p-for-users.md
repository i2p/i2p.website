---
title: "Git over I2P for Users"
date: 2020-03-06
author: "idk"
description: "Git over I2P"
categories: ["development"]
---

Tutorial for setting up git access through an I2P Tunnel. This tunnel will act as your access point to a single git service on I2P. It is part of the overall effort to transition I2P from monotone to Git.

## Before anything else: Know the capabilities the service offers to the public

Depending on how the git service is configured, it may or may not offer all services on the same address. In the case of git.idk.i2p, there is a public HTTP URL, and an SSH URL to configure for your Git SSH client. Either can be used to push or pull, but SSH is recommended.

## First: Set up an account at a Git service

To create your repositories on a remote git service, sign up for a user account at that service. Of course it's also possible to create repositories locally and push them to a remote git service, but most will require an account and for you to create a space for the repository on the server.

## Second: Create a project to test with

To make sure the setup process works, it helps to make a repository to test with from the server. Browse to the i2p-hackers/i2p.i2p repository and fork it to your account.

## Third: Set up your git client tunnel

To have read-write access to a server, you'll need to set up a tunnel for your SSH client. If all you need is read-only HTTP/S cloning, then you can skip all this and just use the http_proxy environment variable to configure git to use the pre-configured I2P HTTP Proxy. For example:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
For SSH access, launch the "New Tunnel Wizard" from http://127.0.0.1:7657/i2ptunnelmgr and set up a client tunnel pointing to the Git service's SSH base32 address.

## Fourth: Attempt a clone

Now your tunnel is all set up, you can attempt a clone over SSH:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
You might get an error where the remote end hangs up unexpectedly. Unfortunately git still doesn't support resumable cloning. Until it does, there are a couple fairly easy ways to handle this. The first and easiest is to try and clone to a shallow depth:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Once you've performed a shallow clone, you can fetch the rest resumably by changing to the repo directory and running:

```
git fetch --unshallow
```
At this point, you still don't have all your branches yet. You can get them by running:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Suggested Workflow for Developers

Revision control works best if you use it well! We strongly suggest a fork-first, feature-branch workflow:

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