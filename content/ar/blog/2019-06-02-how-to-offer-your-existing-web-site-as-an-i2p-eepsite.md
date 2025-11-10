---
title: "How to offer your existing Web Site as an I2P eepSite"
date: 2019-06-02
author: "idk"
description: "Offering an I2P Mirror"
categories: ["tutorial"]
---

This blog post is intended as a general guide to running a mirror of a clear-net service as an eepSite. It elaborates on the previous blog post about basic I2PTunnel tunnels.

Unfortunately, it's probably impossible to *completely* cover all possible cases of making an existing web site available as an eepSite, there's simply too diverse an array of server-side software, not to mention the in-practice peculiarities of any particular deployment of software. Instead, I'm going to try and convey, as specifically as possible, the general process preparing a service for deployment to the eepWeb or other hidden services.

Much of this guide will be treating the reader as a conversational participant, in particular If I really mean it I will address the reader directly(i.e. using "you" instead of "one") and I'll frequently head sections with questions I think the reader might be asking. This is, after all, a "process" that an administrator must consider themselves "involved" in just like hosting any other service.

**DISCLAIMERS:**

While it would be wonderful, it's probably impossible for me to put specific instructions for every single kind of software that one might use to host web sites. As such, this tutorial requires some assumptions on the part of the writer and some critical thinking and common sense on the part of the reader. To be clear, **I have assumed that the person following this tutorial is already operating a clear-web service linkable to a real identity or organization** and thus is simply offering anonymous access and not anonymizing themselves.

Thus, **it makes no attempt whatsoever to anonymize** a connection from one server to another. If you want to run a new, un-linkable hidden service that hosts content not linked to you, then you should not be doing it from your own clearnet server or from your own house.
