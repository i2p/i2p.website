---
title: "I2P on Maven Central"
date: 2016-06-13
author: "str4d"
description: "The I2P client libraries are now available on Maven Central!"
categories: ["summer-dev"]
---

We're nearly half-way into the APIs month of Summer Dev, and making great progress on a number of fronts. I'm happy to announce that the first of these is complete: the I2P client libraries are now available on Maven Central!

This should make it much simpler for Java developers to use I2P in their applications. Instead of needing to obtain the libraries from a current install, they can simply add I2P to their dependencies. Upgrading to new versions will similarly be much easier.

## How to use them

There are two libraries that you need to know about:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Add one or both of these to your project's dependencies, and you're good to go!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```

### Maven

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```

For other build systems, see the Maven Central pages for the core and streaming libraries.

Android developers should use the I2P Android client library, which contains the same libraries along with Android-specific helpers. I'll be updating it soon to depend on the new I2P libraries, so that cross-platform applications can work natively with either I2P Android or desktop I2P.

## Get hacking!

See our application development guide for help getting started with these libraries. You can also chat with us about them in #i2p-dev on IRC. And if you do start using them, let us know what you're working on with the hashtag #I2PSummer on Twitter!
