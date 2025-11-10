---
title: "Naming Discussion"
description: "Historical debate about I2P's naming model and why global DNS-style schemes were rejected"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
aliases:
  - /docs/discussions/naming/
reviewStatus: "needs-review"
---

> **Context:** This page archives long-running debates from the early I2P design era. It captures why the project favoured locally trusted address books over DNS-style lookups or majority-vote registries. For current usage guidance, see the [Naming documentation](/docs/overview/naming/).

## Discarded Alternatives

I2P’s security goals rule out familiar naming schemes:

- **DNS-style resolution.** Any resolver on the lookup path could spoof or censor answers. Even with DNSSEC, compromised registrars or certificate authorities remain a single point of failure. In I2P, destinations *are* public keys—hijacking a lookup would completely compromise an identity.
- **Voting-based naming.** An adversary can mint unlimited identities (a Sybil attack) and “win” votes for popular names. Proof-of-work mitigations raise the cost but introduce heavy coordination overhead.

Instead, I2P deliberately keeps naming above the transport layer. The bundled naming library offers a service-provider interface so alternate schemes can coexist—users decide which address books or jump services they trust.

## Local vs Global Names (jrandom, 2005)

- Names in I2P are **locally unique but human readable**. Your `boss.i2p` may not match somebody else’s `boss.i2p`, and that is by design.
- If a malicious actor tricked you into changing the destination behind a name, they would effectively hijack a service. Refusing global uniqueness prevents that class of attack.
- Treat names like bookmarks or IM nicknames—you choose which destinations to trust by subscribing to specific address books or adding keys manually.

## Common Objections & Responses (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>

## Efficiency Ideas Discussed

- Serve incremental updates (only destinations added since the last fetch).
- Offer supplemental feeds (`recenthosts.cgi`) alongside full hosts files.
- Explore scriptable tooling (for example, `i2host.i2p`) to merge feeds or filter by trust levels.

## Takeaways

- Security wins over global consensus: locally curated address books minimise hijacking risk.
- Multiple naming approaches can coexist through the naming API—users decide what to trust.
- Completely decentralised global naming remains an open research problem; trade-offs among security, human memorability, and global uniqueness still mirror [Zooko’s triangle](https://zooko.com/distnames.html).

## References

- [Naming documentation](/docs/overview/naming/)
- [Zooko’s “Names: Decentralized, Secure, Human-Meaningful: Choose Two”](https://zooko.com/distnames.html)
- Sample incremental feed: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
