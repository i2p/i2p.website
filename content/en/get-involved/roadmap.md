---
title: "I2P Development Roadmap"
description: "Current development plans and historical milestones for the I2P network"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P follows an incremental development model** with releases approximately every 13 weeks. This roadmap covers desktop and Android Java releases in a single, stable release path.

**Last Updated:** August 2025

</div>

## 🎯 Upcoming Releases

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Version 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Target: Early December 2025
</div>

- Hybrid PQ MLKEM Ratchet final, enable by default (prop. 169)
- Jetty 12, require Java 17+
- Continue work on PQ (transports) (prop. 169)
- I2CP lookup support for LS service record parameters (prop. 167)
- Per-tunnel throttling
- Prometheus-friendly stat subsystem
- SAM support for Datagram 2/3

</div>

---

## 📦 Recent Releases

### 2025 Releases

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Released September 8, 2025</span>

- i2psnark UDP tracker support (prop. 160)
- I2CP LS service record parameters (partial) (prop. 167)
- I2CP async lookup API
- Hybrid PQ MLKEM Ratchet Beta (prop. 169)
- Continue work on PQ (transports) (prop. 169)
- Tunnel build bandwidth parameters (prop. 168) Part 2 (handling)
- Continue work on per-tunnel throttling
- Remove unused transport ElGamal code
- Remove ancient SSU2 "active throttle" code
- Remove ancient stat logging support
- Stat/graph subsystem cleanup
- Hidden mode improvements and fixes

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Released June 2, 2025</span>

- Netdb map
- Implement Datagram2, Datagram3 (prop. 163)
- Start work on LS service record parameter (prop. 167)
- Start work on PQ (prop. 169)
- Continue work on per-tunnel throttling
- Tunnel build bandwidth parameters (prop. 168) Part 1 (sending)
- Use /dev/random for PRNG by default on Linux
- Remove redundant LS render code
- Display changelog in HTML
- Reduce HTTP server thread usage
- Fix auto-floodfill enrollment
- Wrapper update to 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Released March 29, 2025</span>

- Fix SHA256 corruption bug

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Released March 17, 2025</span>

- Fix installer failure on Java 21+
- Fix "loopback" bug
- Fix tunnel tests for outbound client tunnels
- Fix installing to paths with spaces
- Update outdated Docker container and container libraries
- Console notification bubbles
- SusiDNS sort-by-latest
- Use SHA256 pool in Noise
- Console dark theme fixes and improvements
- .i2p.alt support

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Released February 3, 2025</span>

- RouterInfo publishing improvements
- Improve SSU2 ACK efficiency
- Improve SSU2 handling of dup relay messages
- Faster / variable lookup timeouts
- LS expiration improvements
- Change symmetric NAT cap
- Enforce POST in more forms
- SusiDNS dark theme fixes
- Bandwidth test cleanups
- New Gan Chinese translation
- Add Kurdish UI option
- New Jammy build
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 2024 Releases</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— October 8, 2024</span>

- i2ptunnel HTTP server reduce thread usage
- Generic UDP Tunnels in I2PTunnel
- Browser Proxy in I2PTunnel
- Website Migration
- Fix for tunnels going yellow
- Console /netdb refactoring

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— August 6, 2024</span>

- Fix iframe size issues in console
- Convert graphs to SVG
- Bundle translation status report

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— July 19, 2024</span>

- Reduce netdb memory usage
- Remove SSU1 code
- Fix i2psnark temp file leaks and stalls
- More efficient PEX in i2psnark
- JS refresh of console graphs
- Graph rendering improvements
- Susimail JS search
- More efficient message handling at OBEP
- More efficient local destination I2CP lookups
- Fix JS variable scoping issues

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— May 15, 2024</span>

- Fix HTTP truncation
- Publish G capability if symmetric NAT detected
- Update to rrd4j 3.9.1-preview

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— May 6, 2024</span>

- NetDB DDoS mitigations
- Tor blocklist
- Susimail fixes and search
- Continue removing SSU1 code
- Update to Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— April 8, 2024</span>

- Console iframe improvements
- Redesign i2psnark bandwidth limiter
- Javascript drag-and-drop for i2psnark and susimail
- i2ptunnel SSL error handling improvements
- i2ptunnel persistent HTTP connection support
- Start removing SSU1 code
- SSU2 relay tag request handling improvements
- SSU2 peer test fixes
- Susimail improvements (loading, markdown, HTML email support)
- Tunnel peer selection adjustments
- Update RRD4J to 3.9
- Update gradlew to 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— December 18, 2023</span>

- NetDB context management/Segmented NetDB
- Handle congestion capabilities by deprioritizing overloaded routers
- Revive Android helper library
- i2psnark local torrent file selector
- NetDB lookup handler fixes
- Disable SSU1
- Ban routers publishing in the future
- SAM fixes
- susimail fixes
- UPnP fixes

</div>

---

### 2023-2022 Releases

<details>
<summary>Click to expand 2023-2022 releases</summary>

**Version 2.3.0** — Released June 28, 2023

- Tunnel peer selection improvements
- User-Configurable blocklist expiration
- Throttle fast bursts of lookup from same source
- Fix replay detection information leak
- NetDB fixes for multihomed leaseSets
- NetDB fixes for leaseSets received as a reply before being received as a store

**Version 2.2.1** — Released April 12, 2023

- Packaging fixes

**Version 2.2.0** — Released March 13, 2023

- Tunnel peer selection improvements
- Streaming replay fix

**Version 2.1.0** — Released January 10, 2023

- SSU2 fixes
- Tunnel build congestion fixes
- SSU peer test and symmetric NAT detection fixes
- Fix broken LS2 encrypted leasesets
- Option to disable SSU 1 (preliminary)
- Compressible padding (proposal 161)
- New console peers status tab
- Add torsocks support to SOCKS proxy and other SOCKS improvements and fixes

**Version 2.0.0** — Released November 21, 2022

- SSU2 connection migration
- SSU2 immediate acks
- Enable SSU2 by default
- SHA-256 digest proxy authentication in i2ptunnel
- Update Android build process to use modern AGP
- Cross-Platform(Desktop) I2P browser auto-configuration support

**Version 1.9.0** — Released August 22, 2022

- SSU2 peer test and relay implementation
- SSU2 fixes
- SSU MTU/PMTU improvements
- Enable SSU2 for a small portion of routers
- Add deadlock detector
- More certificate import fixes
- Fix i2psnark DHT restart after router restart

**Version 1.8.0** — Released May 23, 2022

- Router family fixes and improvements
- Soft restart fixes
- SSU fixes and performance improvements
- I2PSnark standalone fixes and improvements
- Avoid Sybil penalty for trusted families
- Reduce tunnel build reply timeout
- UPnP fixes
- Remove BOB source
- Certificate import fixes
- Tomcat 9.0.62
- Refactoring to support SSU2 (proposal 159)
- Initial implementation of SSU2 base protocol (proposal 159)
- SAM authorization popup for Android apps
- Improve support for custom directory installs in i2p.firefox

**Version 1.7.0** — Released February 21, 2022

- Remove BOB
- New i2psnark torrent editor
- i2psnark standalone fixes and improvements
- NetDB reliability improvements
- Add popup messages in systray
- NTCP2 performance improvements
- Remove outbound tunnel when first hop fails
- Fallback to exploratory for tunnel build reply after repeated client tunnel build failures
- Restore tunnel same-IP restrictions
- Refactor i2ptunnel UDP support for I2CP ports
- Continue work on SSU2, start implementation (proposal 159)
- Create Debian/Ubuntu Package of I2P Browser Profile
- Create Plugin of I2P Browser Profile
- Document I2P for Android applications
- i2pcontrol improvements
- Plugin support improvements
- New local outproxy plugin
- IRCv3 message tag support

</details>

---

### 2021 Releases

<details>
<summary>Click to expand 2021 releases</summary>

**Version 1.6.1** — Released November 29, 2021

- Accelerate rekeying routers to ECIES
- SSU performance improvements
- Improve SSU peer test security
- Add theme selection to new-install wizard
- Continue work on SSU2 (proposal 159)
- Send new tunnel build messages (proposal 157)
- Include automatic browser configuration tool in IzPack installer
- Make Fork-and-Exec Plugins Manageable
- Document jpackage install processes
- Complete, document Go/Java Plugin Generation Tools
- Reseed Plugin for self-signed HTTPS reseed

**Version 1.5.0** — Released August 23, 2021

- Accelerate rekeying routers to ECIES
- Start work on SSU2
- Implement new tunnel build messages (proposal 157)
- Support dmg and exe automatic updates
- New native OSX installer
- X-I2P-Location(alt-svc) locations for built-in I2P Site
- RRD4J 3.8
- Create C, CGo, SWIG bindings for libi2pd

**Version 0.9.50** — Released May 18, 2021

- Accelerate rekeying routers to ECIES
- UPnP IPv6 support
- 4/6 router address caps (proposal 158)
- IPv6 introducers (proposal 158)
- NTP year 2036 fixes
- Continue work on new tunnel build message (proposal 157)
- Enable DoH for reseeding
- Docker improvements
- SSU IPv6 fixes
- Persist Sybil blocklist
- Tunnel bandwidth limiter fixes

**Version 0.9.49** — Released February 17, 2021

- SSU send individual fragments
- SSU Westwood+
- SSU fast retransmit
- SSU fix partial acks
- ECIES router encrypted messages
- Start rekeying routers to ECIES
- Start work on new tunnel build message (proposal 157)
- More SSU performance improvements
- i2psnark webseed support
- Start work on i2psnark hybrid v2 support
- Move web resources to wars
- Move resources to jars
- Fix Gradle build
- Hidden mode fixes
- Change DoH to RFC 8484
- Fix "Start on Boot" support on Android
- Add support for copying b32 addresses on Android
- Add SAMv3 Support to Android
- Revise CSS on default I2P Site
- Document I2P site setup
- Add icons to router console themes
- Complete transition to Git
- Donation page redesign
- Review and update VCS information

</details>

---

### 2020-2016 Historical Archive

<details>
<summary>Click to expand 2020-2016 releases (0.9.48 back to 0.9.24)</summary>

For the complete historical archive of releases from 2020 back to January 2016, including all versions from 0.9.48 to 0.9.24, see the [full release notes](/blog/) on the I2P blog.

**Major milestones from this era:**

- **0.9.47 (August 2020)**: Required Java 8, ECIES enabled for some tunnels, Sybil analysis enabled by default
- **0.9.46 (May 2020)**: Replaced jrobin with rrd4j, ECIES testing
- **0.9.45 (February 2020)**: Full dual IPv4/IPv6 support, hidden mode fixes
- **0.9.44 (December 2019)**: Docker image, testnet Kubernetes, I2P Browser development
- **0.9.43 (October 2019)**: Preliminary ECIES support, SSU IPv6 peer testing, Red25519 signature support
- **0.9.42 (August 2019)**: Browser WebExtensions, Linux distribution ISO
- **0.9.41 (July 2019)**: Redesigned website navigation, router-side meta LS2 support
- **0.9.40 (May 2019)**: Decrypting LS2 support, disable NTCP1, Docker image
- **0.9.39 (March 2019)**: Redesigned website, encrypted LS2 support
- **0.9.38 (January 2019)**: New setup wizard with bandwidth testing, macOS installer enhancements, signed installers
- **0.9.37 (October 2018)**: NTCP2 enabled by default
- **0.9.36 (August 2018)**: NTCP2 implementation (disabled by default)
- **0.9.35 (June 2018)**: Susimail folders, Jetty 9.2.24
- **0.9.34 (April 2018)**: UPnP IGD 2 support, IPv6 improvements
- **0.9.33 (January 2018)**: Reseed proxy support, Jetty 9.2.22, Tomcat 8.5.23
- **0.9.32 (November 2017)**: Ignore hostnames in router infos (proposal 141)
- **0.9.31 (August 2017)**: Console redesign phase 1, i2psnark ratings
- **0.9.30 (May 2017)**: Hidden service server sigtype migration, Tomcat 8 / Jetty 9.2
- **0.9.29 (February 2017)**: Java 9 fixes, NTP hardening, Docker support
- **0.9.28 (December 2016)**: IPv6 improvements, blocklist enhancements
- **0.9.27 (October 2016)**: SSU IPv6 peer testing, hidden mode improvements
- **0.9.26 (June 2016)**: New subscription protocol, Wrapper 3.5.29, GMP 6.0
- **0.9.25 (March 2016)**: SAM v3.3, Sybil tool enhancements, QR codes
- **0.9.24 (January 2016)**: SAM v3.2, Require Java 7, NetDB Family, Ed25519 transition

</details>

---

## Release Information

**Release Cycle:** Approximately every 13 weeks for major releases

**Support Policy:**
- **Current release**: Fully supported with updates and security patches
- **Previous release**: Security updates only
- **Older releases**: No longer supported (upgrade recommended)

**Version Numbering:**
- Started with 0.9.x series (through 0.9.66)
- Transitioned to 1.x series (1.5.0 through 1.9.0)
- Now in 2.x series (2.0.0+)

---

## Development Resources

- **Source Code**: [i2pgit.org](https://i2pgit.org)
- **Issue Tracker**: GitLab issues
- **Monthly Meetings**: First Tuesday of each month
- **IRC**: #i2p-dev on IRC2P
- **Release Notes**: [I2P Blog](/blog/)

---

## Get Involved

Want to contribute to I2P's future? Check out the [Get Involved](/en/get-involved) page to learn how you can help with development, testing, documentation, and more!

For the latest news and detailed release information, visit the [I2P Blog](/en/blog).
