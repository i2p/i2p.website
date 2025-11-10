---
title: "Summer Dev roundup: APIs"
date: 2016-07-02
author: "str4d"
description: "In the first month of Summer Dev, we have improved the usability of our APIs for Java, Android, and Python developers."
categories: ["summer-dev"]
---

Summer Dev is in full swing: we've been busy greasing wheels, sanding edges, and tidying the place up. Now it's time for our first roundup, where we bring you up to speed on the progress we are making!

## APIs month

Our goal for this month was to "blend in" - to make our APIs and libraries work within the existing infrastructure of various communities, so that application developers can work with I2P more efficiently, and users don't need to worry about the details.

### Java / Android

The I2P client libraries are now available on Maven Central! This should make it much simpler for Java developers to use I2P in their applications. Instead of needing to obtain the libraries from a current install, they can simply add I2P to their dependencies. Upgrading to new versions will similarly be much easier.

The I2P Android client library has also been updated to use the new I2P libraries. This means that cross-platform applications can work natively with either I2P Android or desktop I2P.

### Python

#### txi2p

The Twisted plugin `txi2p` now supports in-I2P ports, and will work seamlessly over local, remote, and port-forwarded SAM APIs. See its documentation for usage instructions, and report any issues on GitHub.

#### i2psocket

The first (beta) version of `i2psocket` has been released! This is a direct replacement for the standard Python `socket` library that extends it with I2P support over the SAM API. See its GitHub page for usage instructions, and to report any issues.

### Other progress

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

We are excited to be working with Tahoe-LAFS in July! I2P has for a long time been home to one of the largest public grids, using a patched version of Tahoe-LAFS. During Apps month we will be helping them with their ongoing work to add native support for I2P and Tor, so that I2P users can benefit from all of the improvements upstream.

There are several other projects that we will be talking with about their plans for I2P integration, and helping with design. Stay tuned!

## Take part in Summer Dev!

We have many more ideas for things we'd like to get done in these areas. If you're interested in hacking on privacy and anonymity software, designing usable websites or interfaces, or writing guides for users: come and chat with us on IRC or Twitter! We are always happy to welcome newcomers into our community.

We'll be posting here as we go, but you can also follow our progress, and share your own ideas and work, with the hashtag #I2PSummer on Twitter. Bring on the summer!
