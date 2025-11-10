---
title: "I2P Router Troubleshooting Guide"
description: "Comprehensive troubleshooting guide for common I2P router issues including connectivity, performance, and configuration problems"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

I2P routers fail most commonly due to **port forwarding issues**, **insufficient bandwidth allocation**, and **inadequate bootstrap time**. These three factors account for over 70% of reported problems. The router requires at least **10-15 minutes** after startup to fully integrate into the network, **128 KB/sec minimum bandwidth** (256 KB/sec recommended), and proper **UDP/TCP port forwarding** to achieve non-firewalled status. New users often expect immediate connectivity and restart prematurely, which resets integration progress and creates a frustrating cycle. This guide provides detailed solutions for all major I2P issues affecting versions 2.10.0 and later.

I2P's anonymity architecture inherently trades speed for privacy through multi-hop encrypted tunneling. Understanding this fundamental design helps users set realistic expectations and troubleshoot effectively rather than misinterpreting normal behavior as problems.

## Router won't start or crashes immediately

The most common startup failures stem from **port conflicts**, **Java version incompatibility**, or **corrupted configuration files**. Check if another I2P instance is already running before investigating deeper issues.

**Verify no conflicting processes:**

Linux: `ps aux | grep i2p` or `netstat -tulpn | grep 7657`

Windows: Task Manager → Details → look for java.exe with i2p in command line

macOS: Activity Monitor → search for "i2p"

If a zombie process exists, kill it: `pkill -9 -f i2p` (Linux/Mac) or `taskkill /F /IM javaw.exe` (Windows)

**Check Java version compatibility:**

I2P 2.10.0+ requires **Java 8 minimum**, with Java 11 or later recommended. Verify your installation shows "mixed mode" (not "interpreted mode"):

```bash
java -version
```

Should display: OpenJDK or Oracle Java, version 8+, "mixed mode"

**Avoid:** GNU GCJ, outdated Java implementations, interpreted-only modes

**Common port conflicts** occur when multiple services compete for I2P's default ports. The router console (7657), I2CP (7654), SAM (7656), and HTTP proxy (4444) must be available. Check for conflicts: `netstat -ano | findstr "7657 4444 7654"` (Windows) or `lsof -i :7657,4444,7654` (Linux/Mac).

**Configuration file corruption** manifests as immediate crashes with parse errors in logs. Router.config requires **UTF-8 encoding without BOM**, uses `=` as separator (not `:`), and forbids certain special characters. Back up then examine: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

To reset configuration while preserving identity: Stop I2P, backup router.keys and keyData directory, delete router.config, restart. The router regenerates default configuration.

**Java heap allocation too low** causes OutOfMemoryError crashes. Edit wrapper.config and increase `wrapper.java.maxmemory` from default 128 or 256 to **512 minimum** (1024 for high-bandwidth routers). This requires complete shutdown, waiting 11 minutes, then restart - clicking "Restart" in console won't apply the change.

## Resolving "Network: Firewalled" status

Firewalled status means the router cannot receive direct inbound connections, forcing reliance on introducers. While the router functions in this state, **performance degrades significantly** and network contribution remains minimal. Achieving non-firewalled status requires proper port forwarding.

**The router randomly selects a port** between 9000-31000 for communications. Find your port at http://127.0.0.1:7657/confignet - look for "UDP Port" and "TCP Port" (typically the same number). You must forward **both UDP and TCP** for optimal performance, though UDP alone enables basic functionality.

**Enable UPnP automatic forwarding** (simplest method):

1. Access http://127.0.0.1:7657/confignet
2. Check "Enable UPnP"
3. Save changes and restart router
4. Wait 5-10 minutes and verify status changes from "Network: Firewalled" to "Network: OK"

UPnP requires router support (enabled by default on most consumer routers manufactured after 2010) and proper network configuration.

**Manual port forwarding** (required when UPnP fails):

1. Note your I2P port from http://127.0.0.1:7657/confignet (e.g., 22648)
2. Find your local IP address: `ipconfig` (Windows), `ip addr` (Linux), System Preferences → Network (macOS)
3. Access your router's admin interface (typically 192.168.1.1 or 192.168.0.1)
4. Navigate to Port Forwarding (may be under Advanced, NAT, or Virtual Servers)
5. Create two rules:
   - External Port: [your I2P port] → Internal IP: [your computer] → Internal Port: [same] → Protocol: **UDP**
   - External Port: [your I2P port] → Internal IP: [your computer] → Internal Port: [same] → Protocol: **TCP**
6. Save configuration and restart your router if required

**Verify port forwarding** using online checkers after configuring. If detection fails, check firewall settings - both system firewall and any antivirus firewall must allow the I2P port.

**Hidden mode alternative** for restrictive networks where port forwarding is impossible: Enable at http://127.0.0.1:7657/confignet → check "Hidden mode". The router remains firewalled but optimizes for this state by using SSU introducers exclusively. Performance will be slower but functional.

## Router stuck in "Starting" or "Testing" states

These transient states during initial bootstrap typically resolve within **10-15 minutes for new installations** or **3-5 minutes for established routers**. Premature intervention often worsens problems.

**"Network: Testing"** indicates the router is probing reachability through various connection types (direct, introducers, multiple protocol versions). This is **normal for the first 5-10 minutes** after startup. The router tests multiple scenarios to determine optimal configuration.

**"Rejecting tunnels: starting up"** appears during bootstrap while the router lacks sufficient peer information. The router won't participate in relay traffic until adequately integrated. This message should disappear after 10-20 minutes once netDb populates with 50+ routers.

**Clock skew kills reachability testing.** I2P requires system time within **±60 seconds** of network time. A difference exceeding 90 seconds causes automatic connection rejection. Sync your system clock:

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: Control Panel → Date and Time → Internet Time → Update now → Enable automatic sync

macOS: System Preferences → Date & Time → Enable "Set date and time automatically"

After correcting clock skew, restart I2P completely for proper integration.

**Insufficient bandwidth allocation** prevents successful testing. The router needs adequate capacity to build test tunnels. Configure at http://127.0.0.1:7657/config:

- **Minimum viable:** Inbound 96 KB/sec, Outbound 64 KB/sec
- **Recommended standard:** Inbound 256 KB/sec, Outbound 128 KB/sec  
- **Optimal performance:** Inbound 512+ KB/sec, Outbound 256+ KB/sec
- **Share percentage:** 80% (allows router to contribute bandwidth to network)

Lower bandwidth may work but extends integration time from minutes to hours.

**Corrupted netDb** from improper shutdown or disk errors causes perpetual testing loops. The router can't complete testing without valid peer data:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```

Windows: Delete contents of `%APPDATA%\I2P\netDb\` or `%LOCALAPPDATA%\I2P\netDb\`

**Firewall blocking reseed** prevents acquiring initial peers. During bootstrap, I2P fetches router information from HTTPS reseed servers. Corporate/ISP firewalls may block these connections. Configure reseed proxy at http://127.0.0.1:7657/configreseed if operating behind restrictive networks.

## Slow speeds, timeouts, and tunnel building failures

I2P's design inherently produces **3-10x slower speeds than clearnet** due to multi-hop encryption, packet overhead, and route unpredictability. A tunnel build traverses multiple routers, each adding latency. Understanding this prevents misdiagnosing normal behavior as problems.

**Typical performance expectations:**

- Web browsing .i2p sites: 10-30 second page loads initially, faster after tunnel establishment
- Torrenting via I2PSnark: 10-100 KB/sec per torrent depending on seeders and network conditions  
- Large file downloads: Patience required - megabyte files may take minutes, gigabytes take hours
- First connection slowest: Tunnel building takes 30-90 seconds; subsequent connections use existing tunnels

**Tunnel build success rate** indicates network health. Check at http://127.0.0.1:7657/tunnels:

- **Above 60%:** Normal, healthy operation
- **40-60%:** Marginal, consider bandwidth increase or reducing load
- **Below 40%:** Problematic - indicates insufficient bandwidth, network issues, or poor peer selection

**Increase bandwidth allocation** as first optimization. Most slow performance stems from bandwidth starvation. At http://127.0.0.1:7657/config, increase limits incrementally and monitor graphs at http://127.0.0.1:7657/graphs.

**For DSL/Cable (1-10 Mbps connections):**
- Inbound: 400 KB/sec
- Outbound: 200 KB/sec
- Share: 80%
- Memory: 384 MB (edit wrapper.config)

**For high-speed (10-100+ Mbps connections):**
- Inbound: 1500 KB/sec  
- Outbound: 1000 KB/sec
- Share: 80-100%
- Memory: 512-1024 MB
- Consider: Increase participating tunnels to 2000-5000 at http://127.0.0.1:7657/configadvanced

**Optimize tunnel configuration** for better performance. Access specific tunnel settings at http://127.0.0.1:7657/i2ptunnel and edit each tunnel:

- **Tunnel quantity:** Increase from 2 to 3-4 (more paths available)
- **Backup quantity:** Set to 1-2 (rapid failover if tunnel fails)
- **Tunnel length:** Default 3 hops provides good balance; reducing to 2 improves speed but decreases anonymity

**Native crypto library (jbigi)** provides 5-10x better performance than pure Java encryption. Verify loaded at http://127.0.0.1:7657/logs - look for "jbigi loaded successfully" or "Using native CPUID implementation". If absent:

Linux: Usually auto-detected and loaded from ~/.i2p/jbigi-*.so
Windows: Check for jbigi.dll in I2P installation directory
If missing: Install build tools and compile from source, or download pre-compiled binaries from official repositories

**Keep router running continuously.** Every restart resets integration, requiring 30-60 minutes to rebuild tunnel network and peer relationships. Stable routers with high uptime receive preferential selection for tunnel building, creating positive feedback for performance.

## High CPU and memory consumption

Excessive resource usage typically indicates **inadequate memory allocation**, **missing native crypto libraries**, or **overcommitment to network participation**. Well-configured routers should consume 10-30% CPU during active use and maintain stable memory below 80% of allocated heap.

**Memory problems manifest as:**
- Flat-top memory graphs (pegged at maximum)
- Frequent garbage collection (saw-tooth pattern with steep drops)
- OutOfMemoryError in logs
- Router becoming unresponsive under load
- Automatic shutdown due to resource exhaustion

**Increase Java heap allocation** in wrapper.config (requires complete shutdown):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```

**Critical:** After editing wrapper.config, you **must completely shutdown** (not restart), wait 11 minutes for graceful termination, then start fresh. Router console "Restart" button does not reload wrapper settings.

**CPU optimization requires native crypto library.** Pure Java BigInteger operations consume 10-20x more CPU than native implementations. Verify jbigi status at http://127.0.0.1:7657/logs during startup. Without jbigi, CPU will spike to 50-100% during tunnel building and encryption operations.

**Reduce participating tunnel load** if router overwhelmed:

1. Access http://127.0.0.1:7657/configadvanced
2. Set `router.maxParticipatingTunnels=1000` (default 8000)
3. Lower share percentage at http://127.0.0.1:7657/config from 80% to 50%
4. Disable floodfill mode if enabled: `router.floodfillParticipant=false`

**Limit I2PSnark bandwidth and concurrent torrents.** Torrenting consumes significant resources. At http://127.0.0.1:7657/i2psnark:

- Limit active torrents to 3-5 maximum
- Set "Up BW Limit" and "Down BW Limit" to reasonable values (50-100 KB/sec each)
- Stop torrents when not actively needed
- Avoid seeding dozens of torrents simultaneously

**Monitor resource usage** through built-in graphs at http://127.0.0.1:7657/graphs. Memory should show headroom, not flat-top. CPU spikes during tunnel building are normal; sustained high CPU indicates configuration problems.

**For severely resource-constrained systems** (Raspberry Pi, old hardware), consider **i2pd** (C++ implementation) as alternative. i2pd requires ~130 MB RAM versus 350+ MB for Java I2P, and uses ~7% CPU versus 70% under similar loads. Note that i2pd lacks built-in applications and requires external tools.

## I2PSnark torrent issues

I2PSnark's integration with I2P router architecture requires understanding that **torrenting depends entirely on router tunnel health**. Torrents won't start until the router achieves adequate integration with 10+ active peers and functioning tunnels.

**Torrents stuck at 0% typically indicate:**

1. **Router not fully integrated:** Wait 10-15 minutes after I2P startup before expecting torrent activity
2. **DHT disabled:** Enable at http://127.0.0.1:7657/i2psnark → Configuration → check "Enable DHT" (default enabled since version 0.9.2)
3. **Invalid or dead trackers:** I2P torrents require I2P-specific trackers - clearnet trackers won't work
4. **Insufficient tunnel configuration:** Increase tunnels at I2PSnark Configuration → Tunnels section

**Configure I2PSnark tunnels for better performance:**

- Inbound tunnels: 3-5 (default 2 for Java I2P, 5 for i2pd)
- Outbound tunnels: 3-5  
- Tunnel length: 3 hops (reduce to 2 for speed, less anonymity)
- Tunnel quantity: 3 (provides consistent performance)

**Essential I2P torrent trackers** to include:
- tracker2.postman.i2p (primary, most reliable)
- w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Remove any clearnet (non-.i2p) trackers - they provide no value and create connection attempts that timeout.

**"Torrent not registered" errors** occur when tracker communication fails. Right-click torrent → "Start" forces re-announcement. If persistent, verify tracker accessibility by browsing to http://tracker2.postman.i2p in I2P-configured browser. Dead trackers should be replaced with working alternatives.

**No peers connecting** despite tracker success suggests:
- Router firewalled (improves with port forwarding but not required)
- Insufficient bandwidth (increase to 256+ KB/sec)  
- Swarm too small (some torrents have 1-2 seeders; patience required)
- DHT disabled (enable for trackerless peer discovery)

**Enable DHT and PEX (Peer Exchange)** at I2PSnark Configuration. DHT allows finding peers without tracker dependency. PEX discovers peers from connected peers, accelerating swarm discovery.

**Downloaded files corruption** rarely occurs with I2PSnark's built-in integrity checking. If detected:

1. Right-click torrent → "Check" forces rehash of all pieces
2. Delete corrupted torrent data (keeps .torrent file)  
3. Right-click → "Start" to redownload with piece verification
4. Check disk for errors if corruption persists: `chkdsk` (Windows), `fsck` (Linux)

**Watch directory not working** requires proper configuration:

1. I2PSnark Configuration → "Watch directory": Set absolute path (e.g., `/home/user/torrents/watch`)
2. Ensure I2P process has read permissions: `chmod 755 /path/to/watch`
3. Place .torrent files in watch directory - I2PSnark auto-adds them
4. Configure "Auto start": Check if torrents should start immediately upon addition

**Performance optimization for torrenting:**

- Limit concurrent active torrents: 3-5 maximum for standard connections
- Prioritize important downloads: Stop low-priority torrents temporarily
- Increase router bandwidth allocation: More bandwidth = better torrent performance
- Be patient: I2P torrenting is inherently slower than clearnet BitTorrent
- Seed after downloading: Network thrives on reciprocity

## Git over I2P configuration and troubleshooting

Git operations over I2P require either **SOCKS proxy configuration** or **dedicated I2P tunnels** for SSH/HTTP access. Git's design assumes low-latency connections, making I2P's high-latency architecture challenging.

**Configure Git to use I2P SOCKS proxy:**

Edit ~/.ssh/config (create if absent):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```

This routes all SSH connections to .i2p hosts through I2P's SOCKS proxy (port 4447). The ServerAlive settings maintain connection during I2P latency.

For HTTP/HTTPS git operations, configure git globally:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```

Note: `socks5h` performs DNS resolution through proxy - crucial for .i2p domains.

**Create dedicated I2P tunnel for Git SSH** (more reliable than SOCKS):

1. Access http://127.0.0.1:7657/i2ptunnel
2. "New client tunnel" → "Standard"
3. Configure:
   - Name: Git-SSH  
   - Type: Client
   - Port: 2222 (local port for Git access)
   - Destination: [your-git-server].i2p:22
   - Auto start: Enabled
   - Tunnel count: 3-4 (higher for reliability)
4. Save and start tunnel
5. Configure SSH to use tunnel: `ssh -p 2222 git@127.0.0.1`

**SSH authentication errors** over I2P usually stem from:

- Key not added to ssh-agent: `ssh-add ~/.ssh/id_rsa`
- Wrong key file permissions: `chmod 600 ~/.ssh/id_rsa`
- Tunnel not running: Verify at http://127.0.0.1:7657/i2ptunnel shows green status
- Git server requires specific key type: Generate ed25519 key if RSA fails

**Git operations timing out** relates to I2P's latency characteristics:

- Increase Git timeout: `git config --global http.postBuffer 524288000` (500MB buffer)
- Increase low-speed limit: `git config --global http.lowSpeedLimit 1000` and `git config --global http.lowSpeedTime 600` (waits 10 minutes)
- Use shallow clone for initial checkout: `git clone --depth 1 [url]` (fetches only latest commit, faster)
- Clone during low-activity periods: Network congestion affects I2P performance

**Slow git clone/fetch operations** are inherent to I2P's architecture. A 100MB repository may take 30-60 minutes over I2P versus seconds on clearnet. Strategies:

- Use shallow clones: `--depth 1` dramatically reduces initial data transfer
- Fetch incrementally: Instead of full clone, fetch specific branches: `git fetch origin branch:branch`
- Consider rsync over I2P: For very large repositories, rsync may perform better
- Increase tunnel quantity: More tunnels provide better throughput for sustained large transfers

**"Connection refused" errors** indicate tunnel misconfiguration:

1. Verify I2P router running: Check http://127.0.0.1:7657
2. Confirm tunnel active and green at http://127.0.0.1:7657/i2ptunnel
3. Test tunnel: `nc -zv 127.0.0.1 2222` (should connect if tunnel working)
4. Check destination reachable: Browse to destination's HTTP interface if available
5. Review tunnel logs at http://127.0.0.1:7657/logs for specific errors

**Git over I2P best practices:**

- Keep I2P router running continuously for stable Git access
- Use SSH keys rather than password authentication (fewer interactive prompts)
- Configure persistent tunnels rather than ephemeral SOCKS connections
- Consider hosting your own I2P git server for better control
- Document your .i2p git endpoints for collaborators

## Accessing eepsites and resolving .i2p domains

The most frequent reason users cannot access .i2p sites is **incorrect browser proxy configuration**. I2P sites exist only within the I2P network and require routing through I2P's HTTP proxy.

**Configure browser proxy settings exactly:**

**Firefox (recommended for I2P):**

1. Menu → Settings → Network Settings → Settings button
2. Select "Manual proxy configuration"
3. HTTP Proxy: **127.0.0.1** Port: **4444**
4. SSL Proxy: **127.0.0.1** Port: **4444**  
5. SOCKS Proxy: **127.0.0.1** Port: **4447** (optional, for SOCKS apps)
6. Check "Proxy DNS when using SOCKS v5"
7. OK to save

**Critical Firefox about:config settings:**

Navigate to `about:config` and modify:

- `media.peerconnection.ice.proxy_only` = **true** (prevents WebRTC IP leaks)
- `keyword.enabled` = **false** (prevents .i2p addresses redirecting to search engines)
- `network.proxy.socks_remote_dns` = **true** (DNS through proxy)

**Chrome/Chromium limitations:**

Chrome uses system-wide proxy settings rather than application-specific. On Windows: Settings → search "proxy" → "Open your computer's proxy settings" → Configure HTTP: 127.0.0.1:4444 and HTTPS: 127.0.0.1:4445.

Better approach: Use FoxyProxy or Proxy SwitchyOmega extensions for selective .i2p routing.

**"Website Not Found In Address Book" errors** mean the router lacks the .i2p domain's cryptographic address. I2P uses local addressbooks rather than centralized DNS. Solutions:

**Method 1: Use jump services** (easiest for new sites):

Browse to http://stats.i2p and search for the site. Click the addresshelper link: `http://example.i2p/?i2paddresshelper=base64destination`. Your browser shows "Save to addressbook?" - confirm to add.

**Method 2: Update addressbook subscriptions:**

1. Navigate to http://127.0.0.1:7657/dns (SusiDNS)
2. Click "Subscriptions" tab  
3. Verify active subscriptions (default: http://i2p-projekt.i2p/hosts.txt)
4. Add recommended subscriptions:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Click "Update Now" to force immediate subscription update
6. Wait 5-10 minutes for processing

**Method 3: Use base32 addresses** (always works if site online):

Every .i2p site has a base32 address: 52 random characters followed by .b32.i2p (e.g., `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Base32 addresses bypass addressbook - the router performs direct cryptographic lookup.

**Common browser configuration mistakes:**

- Attempting HTTPS on HTTP-only sites: Most .i2p sites use HTTP only - trying `https://example.i2p` fails
- Forgetting `http://` prefix: Browser may search instead of connecting - always use `http://example.i2p`
- WebRTC enabled: Can leak real IP address - disable via Firefox settings or extensions
- DNS not proxied: Clearnet DNS cannot resolve .i2p - must proxy DNS queries
- Wrong proxy port: 4444 for HTTP (not 4445, which is HTTPS outproxy to clearnet)

**Router not fully integrated** prevents accessing any sites. Verify adequate integration:

1. Check http://127.0.0.1:7657 shows "Network: OK" or "Network: Firewalled" (not "Network: Testing")
2. Active peers shows 10+ minimum (50+ optimal)  
3. No "Rejecting tunnels: starting up" message
4. Wait full 10-15 minutes after router startup before expecting .i2p access

**IRC and email client configuration** follows similar proxy patterns:

**IRC:** Clients connect to **127.0.0.1:6668** (I2P's IRC proxy tunnel). Disable IRC client's proxy settings - connection to localhost:6668 is already proxied through I2P.

**Email (Postman):** 
- SMTP: **127.0.0.1:7659**
- POP3: **127.0.0.1:7660**  
- No SSL/TLS (encryption handled by I2P tunnel)
- Credentials from postman.i2p account registration

All these tunnels must show "running" (green) status at http://127.0.0.1:7657/i2ptunnel.

## Installation failures and package problems

Package-based installations (Debian, Ubuntu, Arch) occasionally fail due to **repository changes**, **GPG key expiration**, or **dependency conflicts**. The official repositories changed from deb.i2p2.de/deb.i2p2.no (end-of-life) to **deb.i2p.net** in recent versions.

**Update Debian/Ubuntu repository to current:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```

**GPG signature verification failures** occur when repository keys expire or change:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```

**Service won't start after package installation** most commonly stems from AppArmor profile issues on Debian/Ubuntu:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```

**Permission problems** on package-installed I2P:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```

**Java compatibility issues:**

I2P 2.10.0 requires **Java 8 minimum**. Older systems may have Java 7 or earlier:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```

**Wrapper configuration errors** prevent service startup:

Wrapper.config location varies by installation method:
- User install: `~/.i2p/wrapper.config`
- Package install: `/etc/i2p/wrapper.config` or `/var/lib/i2p/wrapper.config`

Common wrapper.config problems:

- Incorrect paths: `wrapper.java.command` must point to valid Java installation
- Insufficient memory: `wrapper.java.maxmemory` set too low (increase to 512+)
- Wrong pidfile location: `wrapper.pidfile` must be writable location
- Missing wrapper binary: Some platforms lack precompiled wrapper (use runplain.sh fallback)

**Update failures and corrupted updates:**

Router console updates occasionally fail mid-download due to network interruptions. Manual update procedure:

1. Download i2pupdate_X.X.X.zip from https://geti2p.net/en/download
2. Verify SHA256 checksum matches published hash
3. Copy to I2P install directory as `i2pupdate.zip`
4. Restart router - automatically detects and extracts update
5. Wait 5-10 minutes for update installation
6. Verify new version at http://127.0.0.1:7657

**Migration from very old versions** (pre-0.9.47) to current versions may fail due to incompatible signing keys or removed features. Incremental updates required:

- Versions older than 0.9.9: Cannot verify current signatures - manual update needed
- Versions on Java 6/7: Must upgrade Java before updating I2P to 2.x
- Major version gaps: Update to intermediate version first (0.9.47 recommended waypoint)

**When to use installer vs package:**

- **Packages (apt/yum):** Best for servers, automatic security updates, system integration, systemd management
- **Installer (.jar):** Best for user-level install, Windows, macOS, custom installations, latest version availability

## Configuration file corruption and recovery

I2P's configuration persistence relies on several critical files. Corruption typically results from **improper shutdown**, **disk errors**, or **manual editing mistakes**. Understanding file purposes enables surgical repair rather than complete reinstallation.

**Critical files and their purposes:**

- **router.keys** (516+ bytes): Router's cryptographic identity - losing this creates new identity
- **router.info** (auto-generated): Published router information - safe to delete, regenerates  
- **router.config** (text): Main configuration - bandwidth, network settings, preferences
- **i2ptunnel.config** (text): Tunnel definitions - client/server tunnels, keys, destinations
- **netDb/** (directory): Peer database - router information for network participants
- **peerProfiles/** (directory): Performance statistics on peers - influences tunnel selection
- **keyData/** (directory): Destination keys for eepsites and services - losing changes addresses
- **addressbook/** (directory): Local .i2p hostname mappings

**Complete backup procedure** before modifications:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```

**Router.config corruption symptoms:**

- Router won't start with parse errors in logs
- Settings don't persist after restart
- Unexpected default values appearing  
- Garbled characters when viewing file

**Repair corrupted router.config:**

1. Backup existing: `cp router.config router.config.broken`
2. Check file encoding: Must be UTF-8 without BOM
3. Validate syntax: Keys use `=` separator (not `:`), no trailing spaces on keys, `#` for comments only
4. Common corruption: Non-ASCII characters in values, line ending issues (CRLF vs LF)
5. If unfixable: Delete router.config - router generates default, preserving identity

**Essential router.config settings to preserve:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```

**Lost or invalid router.keys** creates new router identity. This is acceptable unless:

- Running floodfill (loses floodfill status)
- Hosting eepsites with published address (loses continuity)  
- Established reputation in network

No recovery possible without backup - generate new: delete router.keys, restart I2P, new identity created.

**Critical distinction:** router.keys (identity) vs keyData/* (services). Losing router.keys changes router identity. Losing keyData/mysite-keys.dat changes your eepsite's .i2p address - catastrophic if address published.

**Backup eepsite/service keys separately:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```

**NetDb and peerProfiles corruption:**

Symptoms: Zero active peers, can't build tunnels, "Database corruption detected" in logs

Safe fix (all will reseed/rebuild automatically):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```

These directories contain only cached network information - deleting forces fresh bootstrap but loses no critical data.

**Prevention strategies:**

1. **Graceful shutdown always:** Use `i2prouter stop` or router console "Shutdown" button - never force kill
2. **Automated backups:** Cron job weekly backup of ~/.i2p to separate disk
3. **Disk health monitoring:** Check SMART status periodically - failing disks corrupt data
4. **Sufficient disk space:** Maintain 1+ GB free - full disks cause corruption
5. **UPS recommended:** Power failures during writes corrupt files
6. **Version control critical configs:** Git repository for router.config, i2ptunnel.config enables rollback

**File permissions matter:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```

## Common error messages decoded

I2P's logging provides specific error messages that pinpoint problems. Understanding these messages accelerates troubleshooting.

**"No tunnels available"** appears when router hasn't built sufficient tunnels for operation. This is **normal during the first 5-10 minutes** after startup. If persistent beyond 15 minutes:

1. Verify Active Peers > 10 at http://127.0.0.1:7657
2. Check bandwidth allocation adequate (128+ KB/sec minimum)
3. Examine tunnel success rate at http://127.0.0.1:7657/tunnels (should be >40%)
4. Review logs for tunnel build rejection reasons

**"Clock skew detected"** or **"NTCP2 disconnect code 7"** indicates system time differs from network consensus by more than 90 seconds. I2P requires **±60 second accuracy**. Connections with time-divergent routers get automatically rejected.

Fix immediately:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```

**"Build timeout"** or **"Tunnel build timeout exceeded"** means tunnel construction through peer chain didn't complete within timeout window (typically 60 seconds). Causes:

- **Slow peers:** Router selected unresponsive participants for tunnel
- **Network congestion:** I2P network experiencing high load
- **Insufficient bandwidth:** Your bandwidth limits prevent timely tunnel building
- **Overloaded router:** Too many participating tunnels consuming resources

Solutions: Increase bandwidth, reduce participating tunnels (`router.maxParticipatingTunnels` at http://127.0.0.1:7657/configadvanced), enable port forwarding for better peer selection.

**"Router is shutting down"** or **"Graceful shutdown in progress"** appears during normal shutdown or crash recovery. Graceful shutdown can take **up to 10 minutes** as router closes tunnels, notifies peers, and persists state. 

If stuck in shutdown state beyond 11 minutes, force termination:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```

**"java.lang.OutOfMemoryError: Java heap space"** signals heap exhaustion. Immediate solutions:

1. Edit wrapper.config: `wrapper.java.maxmemory=512` (or higher)
2. **Complete shutdown required** - restart won't apply change
3. Wait 11 minutes for full shutdown  
4. Start router fresh
5. Verify memory allocation at http://127.0.0.1:7657/graphs - should show headroom

**Related memory errors:**

- **"GC overhead limit exceeded":** Spending too much time in garbage collection - increase heap
- **"Metaspace":** Java class metadata space exhausted - add `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`

**Windows-specific:** Kaspersky Antivirus limits Java heap to 512MB regardless of wrapper.config settings - uninstall or add I2P to exclusions.

**"Connection timeout"** or **"I2CP Error - port 7654"** when applications try connecting to router:

1. Verify router running: http://127.0.0.1:7657 should respond
2. Check I2CP port: `netstat -an | grep 7654` should show LISTENING
3. Ensure localhost firewall allows: `sudo ufw allow from 127.0.0.1`  
4. Verify application using correct port (I2CP=7654, SAM=7656)

**"Certificate validation failed"** or **"RouterInfo corrupt"** during reseed:

Root causes: Clock skew (fix first), corrupted netDb, invalid reseed certificates

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```

**"Database corruption detected"** indicates disk-level data corruption in netDb or peerProfiles:

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```

Check disk health with SMART tools - recurring corruption suggests failing storage.

## Platform-specific challenges

Different operating systems present unique I2P deployment challenges related to permissions, security policies, and system integration.

### Linux permission and service issues

Package-installed I2P runs as system user **i2psvc** (Debian/Ubuntu) or **i2p** (other distributions), requiring specific permissions:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```

**File descriptor limits** affect router capacity for connections. Default limits (1024) insufficient for high-bandwidth routers:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```

**AppArmor conflicts** common on Debian/Ubuntu prevent service startup:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```

**SELinux issues** on RHEL/CentOS/Fedora:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```

**SystemD service troubleshooting:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```

### Windows firewall and antivirus interference

Windows Defender and third-party antivirus products frequently flag I2P due to network behavior patterns. Proper configuration prevents unnecessary blocks while maintaining security.

**Configure Windows Defender Firewall:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```

Replace port 22648 with your actual I2P port from http://127.0.0.1:7657/confignet.

**Kaspersky Antivirus specific issue:** Kaspersky's "Application Control" limits Java heap to 512MB regardless of wrapper.config settings. This causes OutOfMemoryError on high-bandwidth routers.

Solutions:
1. Add I2P to Kaspersky exclusions: Settings → Additional → Threats and Exclusions → Manage Exclusions
2. Or uninstall Kaspersky (recommended for I2P operation)

**Third-party antivirus general guidance:**

- Add I2P installation directory to exclusions  
- Add %APPDATA%\I2P and %LOCALAPPDATA%\I2P to exclusions
- Exclude javaw.exe from behavioral analysis
- Disable "Network Attack Protection" features that may interfere with I2P protocols

### macOS Gatekeeper blocking installation

macOS Gatekeeper prevents unsigned applications from running. I2P installers aren't signed with Apple Developer ID, triggering security warnings.

**Bypass Gatekeeper for I2P installer:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```

**After installation running** may still trigger warnings:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```

**Never permanently disable Gatekeeper** - security risk for other applications. Use file-specific bypasses only.

**macOS firewall configuration:**

1. System Preferences → Security & Privacy → Firewall → Firewall Options
2. Click "+" to add application  
3. Navigate to Java installation (e.g., `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Add and set to "Allow incoming connections"

### Android I2P application issues

Android version constraints and resource limitations create unique challenges.

**Minimum requirements:**
- Android 5.0+ (API level 21+) required for current versions
- 512MB RAM minimum, 1GB+ recommended  
- 100MB storage for app + router data
- Background app restrictions disabled for I2P

**App crashes immediately:**

1. **Check Android version:** Settings → About Phone → Android version (must be 5.0+)
2. **Uninstall all I2P versions:** Only install one variant:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Multiple installs conflict
3. **Clear app data:** Settings → Apps → I2P → Storage → Clear Data
4. **Reinstall from clean state**

**Battery optimization killing router:**

Android aggressively kills background apps to save battery. I2P needs exclusion:

1. Settings → Battery → Battery optimization (or App battery usage)
2. Find I2P → Don't optimize (or Allow background activity)
3. Settings → Apps → I2P → Battery → Allow background activity + Remove restrictions

**Connection issues on mobile:**

- **Bootstrap requires WiFi:** Initial reseed downloads significant data - use WiFi, not cellular
- **Network changes:** I2P doesn't handle network switches gracefully - restart app after WiFi/cellular transition
- **Bandwidth for mobile:** Configure conservatively at 64-128 KB/sec to avoid cellular data exhaustion

**Performance optimization for mobile:**

1. I2P app → Menu → Settings → Bandwidth
2. Set appropriate limits: 64 KB/sec inbound, 32 KB/sec outbound for cellular
3. Reduce participating tunnels: Settings → Advanced → Max participating tunnels: 100-200
4. Enable "Stop I2P when screen off" for battery conservation

**Torrenting on Android:**

- Limit to 2-3 concurrent torrents maximum
- Reduce DHT aggressiveness  
- Use WiFi only for torrenting
- Accept slower speeds on mobile hardware

## Reseed and bootstrap problems

New I2P installations require **reseeding** - fetching initial peer information from public HTTPS servers to join the network. Reseed problems trap users with zero peers and no network access.

**"No active peers" after fresh install** typically indicates reseed failure. Symptoms:

- Known peers: 0 or stays below 5
- "Network: Testing" persists beyond 15 minutes
- Logs show "Reseed failed" or connection errors to reseed servers

**Why reseed fails:**

1. **Firewall blocking HTTPS:** Corporate/ISP firewalls block reseed server connections (port 443)
2. **SSL certificate errors:** System lacks up-to-date root certificates
3. **Proxy requirement:** Network requires HTTP/SOCKS proxy for external connections
4. **Clock skew:** SSL certificate validation fails when system time wrong
5. **Geographic censorship:** Some countries/ISPs block known reseed servers

**Force manual reseed:**

1. Access http://127.0.0.1:7657/configreseed
2. Click "Save changes and reseed now"  
3. Monitor http://127.0.0.1:7657/logs for "Reseed got XX router infos"
4. Wait 5-10 minutes for processing
5. Check http://127.0.0.1:7657 - Known peers should increase to 50+

**Configure reseed proxy** for restrictive networks:

http://127.0.0.1:7657/configreseed → Proxy Configuration:

- HTTP Proxy: [proxy-server]:[port]
- Or SOCKS5: [socks-server]:[port]  
- Enable "Use proxy for reseed only"
- Credentials if required
- Save and force reseed

**Alternative: Tor proxy for reseed:**

If Tor Browser or Tor daemon running:

- Proxy type: SOCKS5
- Host: 127.0.0.1
- Port: 9050 (default Tor SOCKS port)
- Enable and reseed

**Manual reseed via su3 file** (last resort):

When all automated reseed fails, obtain reseed file out-of-band:

1. Download i2pseeds.su3 from trusted source on unrestricted connection (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. Stop I2P completely
3. Copy i2pseeds.su3 to ~/.i2p/ directory  
4. Start I2P - automatically extracts and processes file
5. Delete i2pseeds.su3 after processing
6. Verify peers increase at http://127.0.0.1:7657

**SSL certificate errors during reseed:**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```

Solutions:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```

**Stuck at 0 known peers beyond 30 minutes:**

Indicates complete reseed failure. Troubleshooting sequence:

1. **Verify system time accurate** (most common issue - fix FIRST)
2. **Test HTTPS connectivity:** Try accessing https://reseed.i2p.rocks in browser - if fails, network issue
3. **Check I2P logs** at http://127.0.0.1:7657/logs for specific reseed errors
4. **Try different reseed URL:** http://127.0.0.1:7657/configreseed → add custom reseed URL: https://reseed-fr.i2pd.xyz/
5. **Use manual su3 file method** if automated attempts exhausted

**Reseed servers occasionally offline:** I2P includes multiple hardcoded reseed servers. If one fails, router tries others automatically. Complete failure of all reseed servers extremely rare but possible.

**Current active reseed servers** (as of October 2025):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Add as custom URLs if having issues with defaults.

**For users in heavily censored regions:**

Consider using Snowflake/Meek bridges through Tor for initial reseed, then switching to direct I2P once integrated. Or obtain i2pseeds.su3 via steganography, email, or USB from outside the censorship zone.

## When to seek additional help

This guide covers the vast majority of I2P issues, but some problems require developer attention or community expertise.

**Seek help from I2P community when:**

- Router crashes consistently after following all troubleshooting steps
- Memory leaks causing steady growth beyond allocated heap
- Tunnel success rate remains below 20% despite adequate configuration  
- New errors in logs not covered by this guide
- Security vulnerabilities discovered
- Feature requests or enhancement suggestions

**Before requesting help, gather diagnostics:**

1. I2P version: http://127.0.0.1:7657 (e.g., "2.10.0")
2. Java version: `java -version` output
3. Operating system and version
4. Router status: Network state, Active peers count, Participating tunnels
5. Bandwidth configuration: Inbound/outbound limits
6. Port forwarding status: Firewalled or OK
7. Relevant log excerpts: Last 50 lines showing errors from http://127.0.0.1:7657/logs

**Official support channels:**

- **Forum:** https://i2pforum.net (clearnet) or http://i2pforum.i2p (within I2P)
- **IRC:** #i2p on Irc2P (irc.postman.i2p via I2P) or irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p for community discussion
- **Bug tracker:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues for confirmed bugs
- **Mailing list:** i2p-dev@lists.i2p-projekt.de for development questions

**Realistic expectations matter.** I2P is slower than clearnet by fundamental design - multi-hop encrypted tunneling creates inherent latency. A working I2P router with 30-second page loads and 50 KB/sec torrent speeds is **functioning correctly**, not broken. Users expecting clearnet speeds will be disappointed regardless of configuration optimization.

## Conclusion

Most I2P problems stem from three categories: insufficient patience during bootstrap (10-15 minutes required), inadequate resource allocation (512 MB RAM, 256 KB/sec bandwidth minimum), or misconfigured port forwarding. Understanding I2P's distributed architecture and anonymity-focused design helps users distinguish expected behavior from actual problems.

The router's "Firewalled" status, while suboptimal, doesn't prevent I2P usage - only limits network contribution and slightly degrades performance. New users should prioritize **stability over optimization**: run the router continuously for several days before adjusting advanced settings, as integration improves naturally with uptime.

When troubleshooting, always verify fundamentals first: correct system time, adequate bandwidth, router running continuously, and 10+ active peers. Most issues resolve by addressing these basics rather than adjusting obscure configuration parameters. I2P rewards patience and continuous operation with improved performance as the router builds reputation and optimizes peer selection over days and weeks of uptime.