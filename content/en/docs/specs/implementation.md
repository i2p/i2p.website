---
title: "Tunnel Operations Guide"
description: "Unified specification for building, encrypting, and transporting traffic with I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Scope:** This guide consolidates the tunnel implementation, message format, and both tunnel creation specifications (ECIES and legacy ElGamal). Existing deep links continue to work through the aliases above.

## Tunnel Model {#tunnel-model}

I2P forwards payloads through *unidirectional tunnels*: ordered sets of routers that carry traffic in a single direction. A full round trip between two destinations requires four tunnels (two outbound, two inbound).

Start with the [Tunnel Overview](/docs/overview/tunnel-routing/) for terminology, then use this guide for the operational details.

### Message Lifecycle {#message-lifecycle}

1. The tunnel **gateway** batches one or more I2NP messages, fragments them, and writes delivery instructions.
2. The gateway encapsulates the payload in a fixed-size (1024&nbsp;B) tunnel message, padding if necessary.
3. Each **participant** verifies the previous hop, applies its encryption layer, and forwards `{nextTunnelId, nextIV, encryptedPayload}` to the next hop.
4. The tunnel **endpoint** removes the final layer, consumes delivery instructions, reassembles fragments, and dispatches the reconstructed I2NP messages.

Duplicate detection uses a decaying Bloom filter keyed by the XOR of the IV and first cipher block to stop tagging attacks based on IV swaps.

### Roles at a Glance {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>

### Encryption Workflow {#encryption-workflow}

- **Inbound tunnels:** the gateway encrypts once with its layer key; downstream participants keep encrypting until the creator decrypts the final payload.
- **Outbound tunnels:** the gateway pre-applies the inverse of each hop’s encryption so that each participant encrypts. When the endpoint encrypts, the gateway’s original plaintext is revealed.

Both directions forward `{tunnelId, IV, encryptedPayload}` to the next hop.

---

## Tunnel Message Format {#tunnel-message-format}

Tunnel gateways fragment I2NP messages into fixed-size envelopes to hide payload length and simplify per-hop processing.

### Encrypted Layout {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```

- **Tunnel ID** – 32-bit identifier for the next hop (non-zero, rotates each build cycle).
- **IV** – 16-byte AES IV chosen per message.
- **Encrypted payload** – 1008 bytes of AES-256-CBC ciphertext.

Total size: 1028 bytes.

### Decrypted Layout {#decrypted-layout}

After a hop removes its encryption layer:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```

- **Checksum** validates the decrypted block.
- **Padding** is random non-zero bytes terminated by a zero byte.
- **Delivery instructions** tell the endpoint how to handle each fragment (locally deliver, forward to another tunnel, etc.).
- **Fragments** carry the underlying I2NP messages; the endpoint reassembles them before passing them to higher layers.

### Processing Steps {#processing-steps}

1. Gateways fragment and queue I2NP messages, retaining partial fragments briefly for reassembly.
2. The gateway encrypts the payload with the appropriate layer keys and installs the tunnel ID plus IV.
3. Each participant encrypts the IV (AES-256/ECB) and then the payload (AES-256/CBC) before re-encrypting the IV and forwarding the message.
4. The endpoint decrypts in reverse order, verifies the checksum, consumes delivery instructions, and reassembles the fragments.

---

## Tunnel Creation (ECIES-X25519) {#tunnel-creation-ecies}

Modern routers build tunnels with ECIES-X25519 keys, shrinking build messages and enabling forward secrecy.

- **Build message:** a single `TunnelBuild` (or `VariableTunnelBuild`) I2NP message carries 1–8 encrypted build records, one per hop.
- **Layer keys:** creators derive per-hop layer, IV, and reply keys via HKDF using the hop’s static X25519 identity and the creator’s ephemeral key.
- **Processing:** each hop decrypts its record, validates request flags, writes the reply block (success or detailed failure code), re-encrypts the remaining records, and forwards the message.
- **Replies:** the creator receives a garlic-wrapped reply message. Records marked as failed include a severity code so the router can profile the peer.
- **Compatibility:** routers may still accept legacy ElGamal builds for backward compatibility, but new tunnels default to ECIES.

> For field-by-field constants and key derivation notes, see the ECIES proposal history and router source; this guide covers the operational flow.

---

## Legacy Tunnel Creation (ElGamal-2048) {#tunnel-creation-elgamal}

The original tunnel build format used ElGamal public keys. Modern routers keep limited support for backward compatibility.

> **Status:** Obsolete. Retained here for historical reference and for anyone maintaining legacy-compatible tooling.

- **Non-interactive telescoping:** a single build message traverses the entire path. Each hop decrypts its 528-byte record, updates the message, and forwards it.
- **Variable length:** the Variable Tunnel Build Message (VTBM) permitted 1–8 records. The earlier fixed message always contained eight records to obscure tunnel length.
- **Request record layout:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```

- **Flags:** bit 7 indicates an inbound gateway (IBGW); bit 6 marks an outbound endpoint (OBEP). They are mutually exclusive.
- **Encryption:** each record is ElGamal-2048 encrypted with the hop’s public key. Symmetric AES-256-CBC layering ensures only the intended hop can read its record.
- **Key facts:** tunnel IDs are non-zero 32-bit values; creators may insert dummy records to hide actual tunnel length; reliability depends on retrying failed builds.

---

## Tunnel Pools and Lifecycle {#tunnel-pools}

Routers maintain independent inbound and outbound tunnel pools for exploratory traffic and for each I2CP session.

- **Peer selection:** exploratory tunnels draw from the “active, not failing” peer bucket to encourage diversity; client tunnels prefer fast, high-capacity peers.
- **Deterministic ordering:** peers are sorted by the XOR distance between `SHA256(peerHash || poolKey)` and the pool’s random key. The key rotates on restart, giving stability within a run while frustrating predecessor attacks across runs.
- **Lifecycle:** routers track historical build times per `{mode, direction, length, variance}` tuple. As tunnels near expiration, replacements begin early; the router increases parallel builds when failures occur while capping outstanding attempts.
- **Configuration knobs:** active/backup tunnel counts, hop length and variance, zero-hop allowances, and build rate limits are all tunable per pool.

---

## Congestion and Reliability {#congestion}

Although tunnels resemble circuits, routers treat them as message queues. Weighted Random Early Discard (WRED) is used to keep latency bounded:

- Drop probability rises as utilisation nears configured limits.
- Participants consider fixed-size fragments; gateways/endpoints drop based on combined fragment size, penalising large payloads first.
- Outbound endpoints drop before other roles to waste the least network effort.

Guaranteed delivery is left to higher layers such as the [Streaming library](/docs/specs/streaming/). Applications that require reliability must handle retransmission and acknowledgments themselves.

---

## Further Reading {#further-reading}


- [Peer Selection](/docs/overview/tunnel-routing#peer-selection/)
- [Tunnel Overview](/docs/overview/tunnel-routing/)
- [Old Tunnel Implementation](/docs/legacy/old-implementation/)
