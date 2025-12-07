---
title: "Network Database Discussion"
description: "Historical notes on floodfill, Kademlia experiments, and future tuning for the netDb"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Note:** This archival discussion outlines historical approaches to the network database (netDb). Consult the [main netDb documentation](/docs/specs/common-structures/) for current behavior and guidance.

## History

I2P's netDb is distributed using a simple floodfill algorithm. Early releases also kept a Kademlia DHT implementation as a fallback, but it proved unreliable and was completely disabled in version 0.6.1.20. The floodfill design forwards a published entry to a participating router, waits for confirmation, and retries with other floodfill peers if necessary. Floodfill peers broadcast stores from non-floodfill routers to every other floodfill participant.

In late 2009 Kademlia lookups were partially reintroduced to reduce the storage burden on individual floodfill routers.

### Introduction of Floodfill

Floodfill first appeared in release 0.6.0.4 while Kademlia remained available as a backup. At the time, heavy packet loss and restricted routes made it difficult to obtain acknowledgements from the four closest peers, often requiring dozens of redundant store attempts. Moving to a floodfill subset of externally reachable routers provided a pragmatic short-term solution.

### Rethinking Kademlia

Some alternatives considered included:

- Running the netDb as a Kademlia DHT limited to reachable routers that opt in to participation
- Retaining the floodfill model but limiting participation to capable routers and verifying distribution with random checks

The floodfill approach won out because it was easier to deploy and the netDb carries only metadata, not user payloads. Most destinations never publish a LeaseSet because the sender typically bundles its LeaseSet in garlic messages.

## Current Status (Historical Perspective)

The netDb algorithms are tuned for the network's needs and have historically handled a few hundred routers comfortably. Early estimates suggested that 3–5 floodfill routers could support roughly 10,000 nodes.

### Updated Calculations (March 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```

Where:

- `N`: Routers in the network
- `L`: Average number of client destinations per router (plus one for the `RouterInfo`)
- `F`: Tunnel failure percentage
- `R`: Tunnel rebuild period as a fraction of tunnel lifetime
- `S`: Average netDb entry size
- `T`: Tunnel lifetime

Using 2008-era values (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) yields:

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```

### Will Kademlia Return?

Developers discussed reintroducing Kademlia around early 2007. The consensus was that floodfill capacity could be expanded incrementally as needed, while Kademlia added significant complexity and resource requirements for the baseline router population. The fallback remains dormant unless floodfill capacity becomes insufficient.

### Floodfill Capacity Planning

Automatic admission of bandwidth-class `O` routers into floodfill, while tempting, risks denial-of-service scenarios if hostile nodes opt in. Historical analysis suggested that limiting the floodfill pool (for example, 3–5 peers handling ~10K routers) was more secure. Trusted operators or automatic heuristics have been used to maintain an adequate yet controlled floodfill set.

## Floodfill TODO (Historical)

> This section is retained for posterity. The main netDb page tracks the current roadmap and design considerations.

Operational incidents, such as a March 13, 2008 period with only one available floodfill router, prompted several improvements delivered in releases 0.6.1.33 through 0.7.x, including:

- Randomizing floodfill selection for searches and preferring responsive peers
- Displaying additional floodfill metrics on the router console "Profiles" page
- Progressive reductions in netDb entry size to cut floodfill bandwidth usage
- Automatic opt-in for a subset of class `O` routers based on performance gathered via profile data
- Enhanced blocklisting, floodfill peer selection, and exploration heuristics

Remaining ideas from the period included:

- Using `dbHistory` statistics to better rate and select floodfill peers
- Improving retry behavior to avoid repeatedly contacting failing peers
- Leveraging latency metrics and integration scores in selection
- Detecting and reacting to failing floodfill routers more quickly
- Continuing to reduce resource demands on high-bandwidth and floodfill nodes

Even as of these notes, the network was considered resilient, with infrastructure in place to respond quickly to hostile floodfills or floodfill-targeted denial-of-service attacks.

## Additional Notes

- The router console has long exposed enhanced profile data to aid in analysing floodfill reliability.
- While historical commentary speculated about Kademlia or alternative DHT schemes, floodfill has remained the primary algorithm for production networks.
- Forward-looking research focused on making floodfill admission adaptive while limiting opportunities for abuse.
