---
title: "New Developer's Guide"
description: "How to start contributing to I2P: study materials, source code, building, ideas, publishing, community, translations, and tools"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - "/en/get-involved/guides/new-developers/"
  - "/get-involved/guides/new-developers/"
type: docs
notes: update translation part
---

So you want to start work on I2P? Great! Here's a quick guide to getting started on contributing to the website or the software, doing development, or creating translations.

Not quite ready for coding? Try [getting involved](/get-involved/) first.

## Get to Know Java

The I2P router and its embedded applications use Java as the main development language. If you don't have experience with Java, you can always have a look at [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)

Study the how intro, other "how" documents, the tech intro, and associated documents:

- How introduction: [Introduction to I2P](/docs/overview/intro/)
- Documentation hub: [Documentation](/docs/)
- Technical introduction: [Technical Introduction](/docs/overview/tech-intro/)

These will give you a good overview of how I2P is structured and what different things it does.

## Getting the I2P Code

For development on the I2P router or the embedded applications, you need to get the source code.

### Our current way: Git

I2P has official Git services and accepts contributions via Git at our own GitLab:

- Inside I2P: <http://git.idk.i2p>
- Outside I2P: <https://i2pgit.org>

Clone the main repository:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```

A read‑only mirror is also available at GitHub:

- GitHub mirror: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```

## Building I2P

To compile the code, you need the Sun/Oracle Java Development Kit 6 or higher, or equivalent JDK (Sun/Oracle JDK 6 strongly recommended) and Apache Ant version 1.7.0 or higher. If you are working on the main I2P code, go into the `i2p.i2p` directory and run `ant` to see the build options.

To build or work on console translations, you need the `xgettext`, `msgfmt`, and `msgmerge` tools from the GNU gettext package.

For development on new applications, see the [application development guide](/get-involved/develop/applications/).

## Development Ideas

See the project TODO list or the issue list on GitLab for ideas:

- GitLab issues: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Making the Results Available

See the bottom of the licenses page for commit privilege requirements. You need these to put code into `i2p.i2p` (not required for the website!).

- [Licenses page](/get-involved/develop/licenses#commit)

## Get to Know Us!

The developers hang around on IRC. They can be reached on various networks and on the I2P internal networks. The usual place to look is `#i2p-dev`. Join the channel and say hi! We also have additional [guidelines for regular developers](/docs/develop/dev-guidelines/).

## Translations

Website and router console translators: See the [New Translator's Guide](/get-involved/guides/new-translators/) for next steps.

## Tools

I2P is open source software that is mostly developed using open‑source toolkits. The I2P project recently acquired a license for the YourKit Java Profiler. Open source projects are eligible to receive a free license provided that YourKit is referenced on the project web site. Please get in touch if you are interested in profiling the I2P codebase.

YourKit is kindly supporting open source projects with its full‑featured profilers. YourKit, LLC is the creator of innovative and intelligent tools for profiling Java and .NET applications. Take a look at YourKit's leading software products:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
