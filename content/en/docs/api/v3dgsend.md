---
title: "v3dgsend"
description: "CLI utility for sending I2P datagrams via SAM v3"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /docs/api/v3dgsend/
---

> Status: This is a concise reference for the `v3dgsend` utility. It complements the [Datagram API](/docs/api/datagrams/) and [SAM v3](/docs/api/samv3/) docs.

## Overview

`v3dgsend` is a command-line helper for sending I2P datagrams using the SAM v3 interface. It is useful for testing datagram delivery, prototyping services, and verifying end-to-end behavior without writing a full client.

Typical uses include:

- Smoke-testing datagram reachability to a Destination
- Validating firewall and address book configuration
- Experimenting with raw vs. signed (repliable) datagrams

## Usage

Basic invocation varies by platform and packaging. Common options include:

- Destination: base64 Destination or `.i2p` name
- Protocol: raw (PROTOCOL 18) or signed (PROTOCOL 17)
- Payload: inline string or file input

Refer to your distribution’s packaging or `--help` output for exact flags.

## See Also

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Library](/docs/api/streaming/) (alternative to datagrams)

