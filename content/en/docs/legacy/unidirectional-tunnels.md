---
title: "Unidirectional Tunnels"
description: "Historical summary of I2P's unidirectional tunnel design."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Historical Notice:** This page preserves the legacy “Unidirectional Tunnels” discussion for reference. Consult the active [tunnel implementation documentation](/docs/specs/implementation/) for current behaviour.

## Overview

I2P builds **unidirectional tunnels**: one tunnel carries outbound traffic and a separate tunnel carries inbound replies. This structure dates to the earliest network designs and remains a key differentiator from bidirectional-circuit systems like Tor. For terminology and implementation details, see the [tunnel overview](/docs/overview/tunnel-routing/) and [tunnel specification](/docs/specs/implementation/).

## Review

- Unidirectional tunnels keep request and response traffic separate, so any single group of colluding peers observes only half of a round trip.
- Timing attacks must intersect two tunnel pools (outbound and inbound) instead of analysing a single circuit, raising the bar for correlation.
- Independent inbound and outbound pools let routers adjust latency, capacity, and failure-handling characteristics per direction.
- Drawbacks include increased peer management complexity and the need to maintain multiple tunnel sets for reliable service delivery.

## Anonymity

Hermann and Grothoff’s paper, [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf), analyses predecessor attacks against unidirectional tunnels, suggesting that determined adversaries can eventually confirm long-lived peers. Community feedback notes that the study relies on specific assumptions about adversary patience and legal powers, and does not weigh the approach against timing attacks that affect bidirectional designs. Continued research and practical experience keep reinforcing unidirectional tunnels as a deliberate anonymity choice rather than an oversight.
