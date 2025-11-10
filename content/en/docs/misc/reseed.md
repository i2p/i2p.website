---
title: "Reseed Hosts"
description: "Operating reseed services and alternate bootstrap methods"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## About Reseed Hosts

New routers need a handful of peers to join the I2P network. Reseed hosts provide that initial bootstrap set over encrypted HTTPS downloads. Each reseed bundle is signed by the host, preventing tampering by unauthenticated parties. Established routers may occasionally reseed if their peer set becomes stale.

### Network Bootstrap Process

When an I2P router first starts or has been offline for an extended period, it requires RouterInfo data to connect to the network. Since the router has no existing peers, it cannot obtain this information from within the I2P network itself. The reseed mechanism solves this bootstrap problem by providing RouterInfo files from trusted external HTTPS servers.

The reseed process delivers 75-100 RouterInfo files in a single cryptographically signed bundle. This ensures new routers can quickly establish connections without exposing them to man-in-the-middle attacks that could isolate them into separate, untrusted network partitions.

### Current Network Status

As of October 2025, the I2P network operates with router version 2.10.0 (API version 0.9.67). The reseed protocol introduced in version 0.9.14 remains stable and unchanged in its core functionality. The network maintains multiple independent reseed servers distributed globally to ensure availability and censorship resistance.

The service [checki2p](https://checki2p.com/reseed) monitors all I2P reseed servers every 4 hours, providing real-time status checks and availability metrics for the reseed infrastructure.

## SU3 File Format Specification

The SU3 file format is the foundation of I2P's reseed protocol, providing cryptographically signed content delivery. Understanding this format is essential for implementing reseed servers and clients.

### File Structure

The SU3 format consists of three main components: header (40+ bytes), content (variable length), and signature (length specified in header).

#### Header Format (Bytes 0-39 minimum)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>

### Reseed-Specific SU3 Parameters

For reseed bundles, the SU3 file must have the following characteristics:

- **File name**: Must be exactly `i2pseeds.su3`
- **Content Type** (byte 27): 0x03 (RESEED)
- **File Type** (byte 25): 0x00 (ZIP)
- **Signature Type** (bytes 8-9): 0x0006 (RSA-4096-SHA512)
- **Version String**: Unix timestamp in ASCII (seconds since epoch, date +%s format)
- **Signer ID**: Email-style identifier matching the X.509 certificate CN

#### Network ID Query Parameter

Since version 0.9.42, routers append `?netid=2` to reseed requests. This prevents cross-network connections, as test networks use different network IDs. The current I2P production network uses network ID 2.

Example request: `https://reseed.example.com/i2pseeds.su3?netid=2`

### ZIP Content Structure

The content section (after the header, before the signature) contains a standard ZIP archive with the following requirements:

- **Compression**: Standard ZIP compression (DEFLATE)
- **File count**: Typically 75-100 RouterInfo files
- **Directory structure**: All files must be at the top level (no subdirectories)
- **File naming**: `routerInfo-{44-character-base64-hash}.dat`
- **Base64 alphabet**: Must use I2P's modified base64 alphabet

The I2P base64 alphabet differs from standard base64 by using `-` and `~` instead of `+` and `/` to ensure filesystem and URL compatibility.

### Cryptographic Signature

The signature covers the entire file from byte 0 through the end of the content section. The signature itself is appended after the content.

#### Signature Algorithm (RSA-4096-SHA512)

1. Compute SHA-512 hash of bytes 0 through end of content
2. Sign the hash using "raw" RSA (NONEwithRSA in Java terminology)
3. Pad signature with leading zeros if necessary to reach 512 bytes
4. Append 512-byte signature to the file

#### Signature Verification Process

Clients must:

1. Read bytes 0-11 to determine signature type and length
2. Read entire header to locate content boundaries
3. Stream content while computing SHA-512 hash
4. Extract signature from end of file
5. Verify signature using signer's RSA-4096 public key
6. Reject file if signature verification fails

### Certificate Trust Model

Reseed signer keys are distributed as self-signed X.509 certificates with RSA-4096 keys. These certificates are included in I2P router packages in the `certificates/reseed/` directory.

Certificate format:
- **Key type**: RSA-4096
- **Signature**: Self-signed
- **Subject CN**: Must match Signer ID in SU3 header
- **Validity dates**: Clients should enforce certificate validity periods

## Running a Reseed Host

Operating a reseed service requires careful attention to security, reliability, and network diversity requirements. More independent reseed hosts increase resilience and make it harder for attackers or censors to block new routers from joining.

### Technical Requirements

#### Server Specifications

- **Operating System**: Unix/Linux (Ubuntu, Debian, FreeBSD tested and recommended)
- **Connectivity**: Static IPv4 address required, IPv6 recommended but optional
- **CPU**: Minimum 2 cores
- **RAM**: Minimum 2 GB
- **Bandwidth**: Approximately 15 GB per month
- **Uptime**: 24/7 operation required
- **I2P Router**: Well-integrated I2P router running continuously

#### Software Requirements

- **Java**: JDK 8 or later (Java 17+ will be required starting with I2P 2.11.0)
- **Web Server**: nginx or Apache with reverse proxy support (Lighttpd no longer supported due to X-Forwarded-For header limitations)
- **TLS/SSL**: Valid TLS certificate (Let's Encrypt, self-signed, or commercial CA)
- **DDoS Protection**: fail2ban or equivalent (mandatory, not optional)
- **Reseed Tools**: Official reseed-tools from https://i2pgit.org/idk/reseed-tools

### Security Requirements

#### HTTPS/TLS Configuration

- **Protocol**: HTTPS only, no HTTP fallback
- **TLS Version**: Minimum TLS 1.2
- **Cipher Suites**: Must support strong ciphers compatible with Java 8+
- **Certificate CN/SAN**: Must match the served URL hostname
- **Certificate Type**: May be self-signed if communicated with dev team, or issued by recognized CA

#### Certificate Management

SU3 signing certificates and TLS certificates serve different purposes:

- **TLS Certificate** (`certificates/ssl/`): Secures HTTPS transport
- **SU3 Signing Certificate** (`certificates/reseed/`): Signs reseed bundles

Both certificates must be provided to the reseed coordinator (zzz@mail.i2p) for inclusion in router packages.

#### DDoS and Scraping Protection

Reseed servers face periodic attacks from buggy implementations, botnets, and malicious actors attempting to scrape the network database. Protection measures include:

- **fail2ban**: Required for rate limiting and attack mitigation
- **Bundle Diversity**: Deliver different RouterInfo sets to different requestors
- **Bundle Consistency**: Deliver same bundle to repeated requests from same IP within configurable time window
- **IP Logging Restrictions**: Do not publicize logs or IP addresses (privacy policy requirement)

### Implementation Methods

#### Method 1: Official reseed-tools (Recommended)

The canonical implementation maintained by the I2P project. Repository: https://i2pgit.org/idk/reseed-tools

**Installation**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```

On first run, the tool will generate:
- `your-email@mail.i2p.crt` (SU3 signing certificate)
- `your-email@mail.i2p.pem` (SU3 signing private key)
- `your-email@mail.i2p.crl` (Certificate revocation list)
- TLS certificate and key files

**Features**:
- Automatic SU3 bundle generation (350 variations, 77 RouterInfos each)
- Built-in HTTPS server
- Rebuild cache every 9 hours via cron
- X-Forwarded-For header support with `--trustProxy` flag
- Compatible with reverse proxy configurations

**Production Deployment**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```

#### Method 2: Python Implementation (pyseeder)

Alternative implementation by PurpleI2P project: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```

#### Method 3: Docker Deployment

For containerized environments, several Docker-ready implementations exist:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Adds Tor onion service and IPFS support

### Reverse Proxy Configuration

#### nginx Configuration

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```

#### Apache Configuration

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```

### Registration and Coordination

To include your reseed server in the official I2P package:

1. Complete setup and testing
2. Send both certificates (SU3 signing and TLS) to the reseed coordinator
3. Contact: zzz@mail.i2p or zzz@i2pmail.org
4. Join #i2p-dev on IRC2P for coordination with other operators

### Operational Best Practices

#### Monitoring and Logging

- Enable Apache/nginx combined log format for statistics
- Implement log rotation (logs grow rapidly)
- Monitor bundle generation success and rebuild times
- Track bandwidth usage and request patterns
- Never publicize IP addresses or detailed access logs

#### Maintenance Schedule

- **Every 9 hours**: Rebuild SU3 bundle cache (automated via cron)
- **Weekly**: Review logs for attack patterns
- **Monthly**: Update I2P router and reseed-tools
- **As needed**: Renew TLS certificates (automate with Let's Encrypt)

#### Port Selection

- Default: 8443 (recommended)
- Alternative: Any port between 1024-49151
- Port 443: Requires root privileges or port forwarding (iptables redirect recommended)

Example port forwarding:
```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```

## Alternative Reseed Methods

Other bootstrap options help users behind restrictive networks:

### File-Based Reseed

Introduced in version 0.9.16, file-based reseeding allows users to manually load RouterInfo bundles. This method is particularly useful for users in censored regions where HTTPS reseed servers are blocked.

**Process**:
1. A trusted contact generates an SU3 bundle using their router
2. Bundle is transferred via email, USB drive, or other out-of-band channel
3. User places `i2pseeds.su3` in I2P configuration directory
4. Router automatically detects and processes the bundle on restart

**Documentation**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Use Cases**:
- Users behind national firewalls blocking reseed servers
- Isolated networks requiring manual bootstrap
- Testing and development environments

### Cloudflare-Proxied Reseeding

Routing reseed traffic through Cloudflare's CDN provides several advantages for operators in high-censorship regions.

**Benefits**:
- Origin server IP address hidden from clients
- DDoS protection via Cloudflare's infrastructure
- Geographic load distribution via edge caching
- Improved performance for global clients

**Implementation Requirements**:
- `--trustProxy` flag enabled in reseed-tools
- Cloudflare proxy enabled for DNS record
- Proper X-Forwarded-For header handling

**Important Considerations**:
- Cloudflare port restrictions apply (must use supported ports)
- Same-client bundle consistency requires X-Forwarded-For support
- SSL/TLS configuration managed by Cloudflare

**Documentation**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Censorship-Resistant Strategies

Research by Nguyen Phong Hoang (USENIX FOCI 2019) identifies additional bootstrap methods for censored networks:

#### Cloud Storage Providers

- **Box, Dropbox, Google Drive, OneDrive**: Host SU3 files on public links
- **Advantage**: Difficult to block without disrupting legitimate services
- **Limitation**: Requires manual URL distribution to users

#### IPFS Distribution

- Host reseed bundles on InterPlanetary File System
- Content-addressed storage prevents tampering
- Resilient to takedown attempts

#### Tor Onion Services

- Reseed servers accessible via .onion addresses
- Resistant to IP-based blocking
- Requires Tor client on user's system

**Research Documentation**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Countries with Known I2P Blocking

As of 2025, the following countries are confirmed to block I2P reseed servers:
- China
- Iran
- Oman
- Qatar
- Kuwait

Users in these regions should utilize alternative bootstrap methods or censorship-resistant reseeding strategies.

## Protocol Details for Implementers

### Reseed Request Specification

#### Client Behavior

1. **Server Selection**: Router maintains hardcoded list of reseed URLs
2. **Random Selection**: Client randomly selects server from available list
3. **Request Format**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Should mimic common browsers (e.g., "Wget/1.11.4")
5. **Retry Logic**: If SU3 request fails, fall back to index page parsing
6. **Certificate Validation**: Verify TLS certificate against system trust store
7. **SU3 Signature Validation**: Verify signature against known reseed certificates

#### Server Behavior

1. **Bundle Selection**: Select pseudo-random subset of RouterInfos from netDb
2. **Client Tracking**: Identify requests by source IP (respecting X-Forwarded-For)
3. **Bundle Consistency**: Return same bundle to repeat requests within time window (typically 8-12 hours)
4. **Bundle Diversity**: Return different bundles to different clients for network diversity
5. **Content-Type**: `application/octet-stream` or `application/x-i2p-reseed`

### RouterInfo File Format

Each `.dat` file in the reseed bundle contains a RouterInfo structure:

**File Naming**: `routerInfo-{base64-hash}.dat`
- Hash is 44 characters using I2P base64 alphabet
- Example: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**File Contents**:
- RouterIdentity (router hash, encryption key, signing key)
- Publication timestamp
- Router addresses (IP, port, transport type)
- Router capabilities and options
- Signature covering all above data

### Network Diversity Requirements

To prevent network centralization and enable Sybil attack detection:

- **No complete NetDb dumps**: Never serve all RouterInfos to single client
- **Random sampling**: Each bundle contains different subset of available peers
- **Minimum bundle size**: 75 RouterInfos (increased from original 50)
- **Maximum bundle size**: 100 RouterInfos
- **Freshness**: RouterInfos should be recent (within 24 hours of generation)

### IPv6 Considerations

**Current Status** (2025):
- Several reseed servers show IPv6 unresponsiveness
- Clients should prefer or force IPv4 for reliability
- IPv6 support is recommended for new deployments but not critical

**Implementation Note**: When configuring dual-stack servers, ensure both IPv4 and IPv6 listen addresses function correctly, or disable IPv6 if it cannot be properly supported.

## Security Considerations

### Threat Model

The reseed protocol defends against:

1. **Man-in-the-middle attacks**: RSA-4096 signatures prevent bundle tampering
2. **Network partitioning**: Multiple independent reseed servers prevent single point of control
3. **Sybil attacks**: Bundle diversity limits attacker's ability to isolate users
4. **Censorship**: Multiple servers and alternative methods provide redundancy

The reseed protocol does NOT defend against:

1. **Compromised reseed servers**: If attacker controls reseed certificate private keys
2. **Complete network blocking**: If all reseed methods are blocked in a region
3. **Long-term monitoring**: Reseed requests reveal IP attempting to join I2P

### Certificate Management

**Private Key Security**:
- Store SU3 signing keys offline when not in use
- Use strong passwords for key encryption
- Maintain secure backups of keys and certificates
- Consider hardware security modules (HSMs) for high-value deployments

**Certificate Revocation**:
- Certificate Revocation Lists (CRLs) distributed via news feed
- Compromised certificates can be revoked by coordinator
- Routers automatically update CRLs with software updates

### Attack Mitigation

**DDoS Protection**:
- fail2ban rules for excessive requests
- Rate limiting at web server level
- Connection limits per IP address
- Cloudflare or similar CDN for additional layer

**Scraping Prevention**:
- Different bundles per requesting IP
- Time-based bundle caching per IP
- Logging patterns that indicate scraping attempts
- Coordination with other operators on detected attacks

## Testing and Validation

### Testing Your Reseed Server

#### Method 1: Fresh Router Install

1. Install I2P on clean system
2. Add your reseed URL to configuration
3. Remove or disable other reseed URLs
4. Start router and monitor logs for successful reseed
5. Verify connection to network within 5-10 minutes

Expected log output:
```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```

#### Method 2: Manual SU3 Validation

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```

#### Method 3: checki2p Monitoring

The service at https://checki2p.com/reseed performs automated checks every 4 hours on all registered I2P reseed servers. This provides:

- Availability monitoring
- Response time metrics
- TLS certificate validation
- SU3 signature verification
- Historical uptime data

Once your reseed is registered with the I2P project, it will automatically appear on checki2p within 24 hours.

### Troubleshooting Common Issues

**Issue**: "Unable to read signing key" on first run
- **Solution**: This is expected. Answer 'y' to generate new keys.

**Issue**: Router fails to verify signature
- **Cause**: Certificate not in router's trust store
- **Solution**: Place certificate in `~/.i2p/certificates/reseed/` directory

**Issue**: Same bundle delivered to different clients
- **Cause**: X-Forwarded-For header not properly forwarded
- **Solution**: Enable `--trustProxy` and configure reverse proxy headers

**Issue**: "Connection refused" errors
- **Cause**: Port not accessible from internet
- **Solution**: Check firewall rules, verify port forwarding

**Issue**: High CPU usage during bundle rebuild
- **Cause**: Normal behavior when generating 350+ SU3 variations
- **Solution**: Ensure adequate CPU resources, consider reducing rebuild frequency

## Reference Information

### Official Documentation

- **Reseed Contributors Guide**: /guides/creating-and-running-an-i2p-reseed-server/
- **Reseed Policy Requirements**: /guides/reseed-policy/
- **SU3 Specification**: /docs/specs/updates/
- **Reseed Tools Repository**: https://i2pgit.org/idk/reseed-tools
- **Reseed Tools Documentation**: https://eyedeekay.github.io/reseed-tools/

### Alternative Implementations

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder**: https://github.com/torbjo/i2p-reseeder

### Community Resources

- **I2P Forum**: https://i2pforum.net/
- **Gitea Repository**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev on IRC2P
- **Status Monitoring**: https://checki2p.com/reseed

### Version History

- **0.9.14** (2014): SU3 reseed format introduced
- **0.9.16** (2014): File-based reseeding added
- **0.9.42** (2019): Network ID query parameter requirement
- **2.0.0** (2022): SSU2 transport protocol introduced
- **2.4.0** (2024): NetDB isolation and security improvements
- **2.6.0** (2024): I2P-over-Tor connections blocked
- **2.10.0** (2025): Current stable release (as of September 2025)

### Signature Type Reference

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>

**Reseed Standard**: Type 6 (RSA-SHA512-4096) is required for reseed bundles.

## Appreciation

Thanks to every reseed operator for keeping the network accessible and resilient. Special recognition to the following contributors and projects:

- **zzz**: Long-time I2P developer and reseed coordinator
- **idk**: Current maintainer of reseed-tools and release manager
- **Nguyen Phong Hoang**: Research on censorship-resistant reseeding strategies
- **PurpleI2P Team**: Alternative I2P implementations and tools
- **checki2p**: Automated monitoring service for reseed infrastructure

The I2P network's decentralized reseed infrastructure represents a collaborative effort by dozens of operators worldwide, ensuring that new users can always find a path to join the network regardless of local censorship or technical barriers.
