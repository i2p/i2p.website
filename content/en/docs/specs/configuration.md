---
title: "Router Configuration"
description: "Configuration options and formats for I2P routers and clients"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---
## Overview

This document provides a comprehensive technical specification of I2P configuration files used by the router and various applications. It covers file format specifications, property definitions, and implementation details verified against the I2P source code and official documentation.

### Scope

- Router configuration files and formats
- Client application configurations
- I2PTunnel tunnel configurations
- File format specifications and implementation
- Version-specific features and deprecations

### Implementation Notes

Configuration files are read and written using `DataHelper.loadProps()` and `storeProps()` methods in the I2P core library. The file format differs significantly from the serialized format used in I2P protocols (see [Common Structures Specification - Type Mapping](/docs/specs/common-structures/#type-mapping)).

---

## General Configuration File Format

I2P configuration files follow a modified Java Properties format with specific exceptions and constraints.

### Format Specification

Based on [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) with the following critical differences:

#### Encoding
- **MUST** use UTF-8 encoding (NOT ISO-8859-1 as in standard Java Properties)
- Implementation: Uses `DataHelper.getUTF8()` utilities for all file operations

#### Escape Sequences
- **NO** escape sequences are recognized (including backslash `\`)
- Line continuation is **NOT** supported
- Backslash characters are treated as literal

#### Comment Characters
- `#` starts a comment in any position on a line
- `;` starts a comment **only** when in column 1
- `!` does **NOT** start a comment (differs from Java Properties)

#### Key-Value Separators
- `=` is the **ONLY** valid key-value separator
- `:` is **NOT** recognized as a separator
- Whitespace is **NOT** recognized as a separator

#### Whitespace Handling
- Leading and trailing whitespace is **NOT** trimmed on keys
- Leading and trailing whitespace **IS** trimmed on values

#### Line Processing
- Lines without `=` are ignored (treated as comments or blank lines)
- Empty values (`key=`) are supported as of version 0.9.10
- Keys with empty values are stored and retrieved normally

#### Character Restrictions

**Keys may NOT contain**:
- `#` (hash/pound sign)
- `=` (equals sign)
- `\n` (newline character)
- Cannot start with `;` (semicolon)

**Values may NOT contain**:
- `#` (hash/pound sign)
- `\n` (newline character)
- Cannot start or end with `\r` (carriage return)
- Cannot start or end with whitespace (trimmed automatically)

### File Sorting

Configuration files need not be sorted by key. However, most I2P applications sort keys alphabetically when writing configuration files to facilitate:
- Manual editing
- Version control diff operations
- Human readability

### Implementation Details

#### Reading Configuration Files

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```

**Behavior**:
- Reads UTF-8 encoded files
- Enforces all format rules described above
- Validates character restrictions
- Returns empty Properties object if file doesn't exist
- Throws `IOException` for read errors

#### Writing Configuration Files

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```

**Behavior**:
- Writes UTF-8 encoded files
- Sorts keys alphabetically (unless OrderedProperties used)
- Sets file permissions to mode 600 (user read/write only) as of version 0.8.1
- Throws `IllegalArgumentException` for invalid characters in keys or values
- Throws `IOException` for write errors

#### Format Validation

The implementation performs strict validation:
- Keys and values are checked for prohibited characters
- Invalid entries cause exceptions during write operations
- Reading silently ignores malformed lines (lines without `=`)

### Format Examples

#### Valid Configuration File

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```

#### Invalid Configuration Examples

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```

---

## Core Library and Router Configuration

### Clients Configuration (clients.config)

**Location**: `$I2P_CONFIG_DIR/clients.config` (legacy) or `$I2P_CONFIG_DIR/clients.config.d/` (modern)  
**Configuration Interface**: Router console at `/configclients`  
**Format Change**: Version 0.9.42 (August 2019)

#### Directory Structure (Version 0.9.42+)

As of release 0.9.42, the default clients.config file is automatically split into individual configuration files:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```

**Migration Behavior**:
- On first run after upgrade to 0.9.42+, monolithic file is split automatically
- Properties in split files are prefixed with `clientApp.0.`
- Legacy format still supported for backward compatibility
- Split format enables modular packaging and plugin management

#### Property Format

Lines are of the form `clientApp.x.prop=val`, where `x` is the app number.

**App numbering requirements**:
- MUST start with 0
- MUST be consecutive (no gaps)
- Order determines startup sequence

#### Required Properties

##### main
- **Type**: String (fully qualified class name)
- **Required**: Yes
- **Description**: The constructor or `main()` method in this class will be invoked depending on client type (managed vs. unmanaged)
- **Example**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Optional Properties

##### name
- **Type**: String
- **Required**: No
- **Description**: Display name shown in router console
- **Example**: `clientApp.0.name=Router Console`

##### args
- **Type**: String (space or tab separated)
- **Required**: No
- **Description**: Arguments passed to main class constructor or main() method
- **Quoting**: Arguments containing spaces or tabs may be quoted with `'` or `"`
- **Example**: `clientApp.0.args=-d $CONFIG/eepsite`

##### delay
- **Type**: Integer (seconds)
- **Required**: No
- **Default**: 120
- **Description**: Seconds to wait before starting the client
- **Overrides**: Overridden by `onBoot=true` (sets delay to 0)
- **Special Values**:
  - `< 0`: Wait for router to reach RUNNING state, then start immediately in new thread
  - `= 0`: Run immediately in same thread (exceptions propagate to console)
  - `> 0`: Start after delay in new thread (exceptions logged, not propagated)

##### onBoot
- **Type**: Boolean
- **Required**: No
- **Default**: false
- **Description**: Forces delay of 0, overrides explicit delay setting
- **Use Case**: Start critical services immediately at router boot

##### startOnLoad
- **Type**: Boolean
- **Required**: No
- **Default**: true
- **Description**: Whether to start the client at all
- **Use Case**: Disable clients without removing configuration

#### Plugin-Specific Properties

These properties are used only by plugins (not core clients):

##### stopargs
- **Type**: String (space or tab separated)
- **Description**: Arguments passed to stop the client
- **Variable Substitution**: Yes (see below)

##### uninstallargs
- **Type**: String (space or tab separated)
- **Description**: Arguments passed to uninstall the client
- **Variable Substitution**: Yes (see below)

##### classpath
- **Type**: String (comma-separated paths)
- **Description**: Additional classpath elements for the client
- **Variable Substitution**: Yes (see below)

#### Variable Substitution (Plugins Only)

The following variables are substituted in `args`, `stopargs`, `uninstallargs`, and `classpath` for plugins:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>

**Note**: Variable substitution is performed only for plugins, not for core clients.

#### Client Types

##### Managed Clients
- Constructor is called with `RouterContext` and `ClientAppManager` parameters
- Client must implement `ClientApp` interface
- Lifecycle controlled by router
- Can be started, stopped, and restarted dynamically

##### Unmanaged Clients
- `main(String[] args)` method is called
- Run in separate thread
- Lifecycle not managed by router
- Legacy client type

#### Example Configuration

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```

---

### Logger Configuration (logger.config)

**Location**: `$I2P_CONFIG_DIR/logger.config`  
**Configuration Interface**: Router console at `/configlogging`

#### Properties Reference

##### Console Buffer Configuration

###### logger.consoleBufferSize
- **Type**: Integer
- **Default**: 20
- **Description**: Maximum number of log messages to buffer in console
- **Range**: 1-1000 recommended

##### Date and Time Formatting

###### logger.dateFormat
- **Type**: String (SimpleDateFormat pattern)
- **Default**: From system locale
- **Example**: `HH:mm:ss.SSS`
- **Documentation**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Log Levels

###### logger.defaultLevel
- **Type**: Enum
- **Default**: ERROR
- **Values**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Description**: Default logging level for all classes

###### logger.minimumOnScreenLevel
- **Type**: Enum
- **Default**: CRIT
- **Values**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Description**: Minimum level for messages shown on screen

###### logger.record.{class}
- **Type**: Enum
- **Values**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Description**: Per-class logging level override
- **Example**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Display Options

###### logger.displayOnScreen
- **Type**: Boolean
- **Default**: true
- **Description**: Whether to display log messages in console output

###### logger.dropDuplicates
- **Type**: Boolean
- **Default**: true
- **Description**: Drop duplicate consecutive log messages

###### logger.dropOnOverflow
- **Type**: Boolean
- **Default**: false
- **Description**: Drop messages when buffer is full (vs. blocking)

##### Flushing Behavior

###### logger.flushInterval
- **Type**: Integer (seconds)
- **Default**: 29
- **Since**: Version 0.9.18
- **Description**: How often to flush log buffer to disk

##### Format Configuration

###### logger.format
- **Type**: String (character sequence)
- **Description**: Log message format template
- **Format Characters**:
  - `d` = date/time
  - `c` = class name
  - `t` = thread name
  - `p` = priority (log level)
  - `m` = message
- **Example**: `dctpm` produces `[timestamp] [class] [thread] [level] message`

##### Compression (Version 0.9.56+)

###### logger.gzip
- **Type**: Boolean
- **Default**: false
- **Since**: Version 0.9.56
- **Description**: Enable gzip compression for rotated log files

###### logger.minGzipSize
- **Type**: Integer (bytes)
- **Default**: 65536
- **Since**: Version 0.9.56
- **Description**: Minimum file size to trigger compression (64 KB default)

##### File Management

###### logger.logBufferSize
- **Type**: Integer (bytes)
- **Default**: 1024
- **Description**: Maximum messages to buffer before flushing

###### logger.logFileName
- **Type**: String (file path)
- **Default**: `logs/log-@.txt`
- **Description**: Log file naming pattern (`@` replaced with rotation number)

###### logger.logFilenameOverride
- **Type**: String (file path)
- **Description**: Override for log file name (disables rotation pattern)

###### logger.logFileSize
- **Type**: String (size with unit)
- **Default**: 10M
- **Units**: K (kilobytes), M (megabytes), G (gigabytes)
- **Example**: `50M`, `1G`

###### logger.logRotationLimit
- **Type**: Integer
- **Default**: 2
- **Description**: Highest rotation file number (log-0.txt through log-N.txt)

#### Example Configuration

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```

---

### Plugin Configuration

#### Individual Plugin Configuration (plugins/*/plugin.config)

**Location**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`  
**Format**: Standard I2P configuration file format  
**Documentation**: [Plugin Specification](/docs/specs/plugin/)

##### Required Properties

###### name
- **Type**: String
- **Required**: Yes
- **Description**: Plugin display name
- **Example**: `name=I2P Plugin Example`

###### key
- **Type**: String (public key)
- **Required**: Yes (omit for SU3 signed plugins)
- **Description**: Plugin signing public key for verification
- **Format**: Base64-encoded signing key

###### signer
- **Type**: String
- **Required**: Yes
- **Description**: Plugin signer identity
- **Example**: `signer=user@example.i2p`

###### version
- **Type**: String (VersionComparator format)
- **Required**: Yes
- **Description**: Plugin version for update checking
- **Format**: Semantic versioning or custom comparable format
- **Example**: `version=1.2.3`

##### Display Properties

###### date
- **Type**: Long (Unix timestamp milliseconds)
- **Description**: Plugin release date

###### author
- **Type**: String
- **Description**: Plugin author name

###### websiteURL
- **Type**: String (URL)
- **Description**: Plugin website URL

###### updateURL
- **Type**: String (URL)
- **Description**: Update check URL for plugin

###### updateURL.su3
- **Type**: String (URL)
- **Since**: Version 0.9.15
- **Description**: SU3 format update URL (preferred)

###### description
- **Type**: String
- **Description**: English plugin description

###### description_{language}
- **Type**: String
- **Description**: Localized plugin description
- **Example**: `description_de=Deutsche Beschreibung`

###### license
- **Type**: String
- **Description**: Plugin license identifier
- **Example**: `license=Apache 2.0`

##### Installation Properties

###### dont-start-at-install
- **Type**: Boolean
- **Default**: false
- **Description**: Prevent automatic start after installation

###### router-restart-required
- **Type**: Boolean
- **Default**: false
- **Description**: Require router restart after installation

###### install-only
- **Type**: Boolean
- **Default**: false
- **Description**: Install once only (no updates)

###### update-only
- **Type**: Boolean
- **Default**: false
- **Description**: Update existing installation only (no fresh install)

##### Example Plugin Configuration

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```

#### Global Plugin Configuration (plugins.config)

**Location**: `$I2P_CONFIG_DIR/plugins.config`  
**Purpose**: Enable/disable installed plugins globally

##### Property Format

```properties
plugin.{name}.startOnLoad=true|false
```

- `{name}`: Plugin name from plugin.config
- `startOnLoad`: Whether to start plugin at router launch

##### Example

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```

---

### Web Applications Configuration (webapps.config)

**Location**: `$I2P_CONFIG_DIR/webapps.config`  
**Purpose**: Enable/disable and configure web applications

#### Property Format

##### webapps.{name}.startOnLoad
- **Type**: Boolean
- **Description**: Whether to start webapp at router launch
- **Format**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath
- **Type**: String (space or comma-separated paths)
- **Description**: Additional classpath elements for webapp
- **Format**: `webapps.{name}.classpath=[paths]`

#### Variable Substitution

Paths support the following variable substitutions:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>

#### Classpath Resolution

- **Core webapps**: Paths relative to `$I2P/lib`
- **Plugin webapps**: Paths relative to `$CONFIG/plugins/{appname}/lib`

#### Example Configuration

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```

---

### Router Configuration (router.config)

**Location**: `$I2P_CONFIG_DIR/router.config`  
**Configuration Interface**: Router console at `/configadvanced`  
**Purpose**: Core router settings and network parameters

#### Configuration Categories

##### Network Configuration

Bandwidth settings:
```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```

Transport configuration:
```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```

##### Router Behavior

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```

##### Console Configuration

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```

##### Time Configuration

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```

**Note**: Router configuration is extensive. See router console at `/configadvanced` for complete property reference.

---

## Application Configuration Files

### Address Book Configuration (addressbook/config.txt)

**Location**: `$I2P_CONFIG_DIR/addressbook/config.txt`  
**Application**: SusiDNS  
**Purpose**: Hostname resolution and address book management

#### File Locations

##### router_addressbook
- **Default**: `../hosts.txt`
- **Description**: Master address book (system-wide hostnames)
- **Format**: Standard hosts file format

##### privatehosts.txt
- **Location**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Description**: Private hostname mappings
- **Priority**: Highest (overrides all other sources)

##### userhosts.txt
- **Location**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Description**: User-added hostname mappings
- **Management**: Via SusiDNS interface

##### hosts.txt
- **Location**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Description**: Downloaded public address book
- **Source**: Subscription feeds

#### Naming Service

##### BlockfileNamingService (Default since 0.8.8)

Storage format:
- **File**: `hostsdb.blockfile`
- **Location**: `$I2P_CONFIG_DIR/addressbook/`
- **Performance**: ~10x faster lookups than hosts.txt
- **Format**: Binary database format

Legacy naming service:
- **Format**: Plain text hosts.txt
- **Status**: Deprecated but still supported
- **Use Case**: Manual editing, version control

#### Hostname Rules

I2P hostnames must conform to:

1. **TLD requirement**: Must end with `.i2p`
2. **Maximum length**: 67 characters total
3. **Character set**: `[a-z]`, `[0-9]`, `.` (period), `-` (hyphen)
4. **Case**: Lowercase only
5. **Start restrictions**: Cannot start with `.` or `-`
6. **Forbidden patterns**: Cannot contain `..`, `.-`, or `-.` (since 0.6.1.33)
7. **Reserved**: Base32 hostnames `*.b32.i2p` (52 chars of base32.b32.i2p)

##### Valid Examples
```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```

##### Invalid Examples
```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```

#### Subscription Management

##### subscriptions.txt
- **Location**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Format**: One URL per line
- **Default**: `http://i2p-projekt.i2p/hosts.txt`

##### Subscription Feed Format (Since 0.9.26)

Advanced feed format with metadata:
```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```

Metadata properties:
- `added`: Date hostname was added (YYYYMMDD format)
- `src`: Source identifier
- `sig`: Optional signature

**Backward compatibility**: Simple hostname=destination format still supported.

#### Example Configuration

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```

---

### I2PSnark Configuration (i2psnark.config.d/i2psnark.config)

**Location**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`  
**Application**: I2PSnark BitTorrent client  
**Configuration Interface**: Web GUI at http://127.0.0.1:7657/i2psnark

#### Directory Structure

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```

#### Main Configuration (i2psnark.config)

Minimal default configuration:
```properties
i2psnark.dir=i2psnark
```

Additional properties managed via web interface:
```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```

#### Individual Torrent Configuration

**Location**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`  
**Format**: Per-torrent settings  
**Management**: Automatic (via web GUI)

Properties include:
- Torrent-specific upload/download settings
- File priorities
- Tracker information
- Peer limits

**Note**: Torrent configurations are primarily managed through the web interface. Manual editing is not recommended.

#### Torrent Data Organization

Data storage is separate from configuration:
```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```

---

### I2PTunnel Configuration (i2ptunnel.config)

**Location**: `$I2P_CONFIG_DIR/i2ptunnel.config` (legacy) or `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (modern)  
**Configuration Interface**: Router console at `/i2ptunnel`  
**Format Change**: Version 0.9.42 (August 2019)

#### Directory Structure (Version 0.9.42+)

As of release 0.9.42, the default i2ptunnel.config file is automatically split:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```

**Critical Format Difference**:
- **Monolithic format**: Properties prefixed with `tunnel.N.`
- **Split format**: Properties **NOT** prefixed (e.g., `description=`, not `tunnel.0.description=`)

#### Migration Behavior

On first run after upgrade to 0.9.42:
1. Existing i2ptunnel.config is read
2. Individual tunnel configs created in i2ptunnel.config.d/
3. Properties are de-prefixed in split files
4. Original file backed up
5. Legacy format still supported for backward compatibility

#### Configuration Sections

The I2PTunnel configuration is documented in detail in the [I2PTunnel Configuration Reference](#i2ptunnel-configuration-reference) section below. Property descriptions are applicable to both monolithic (`tunnel.N.property`) and split (`property`) formats.

---

## I2PTunnel Configuration Reference

This section provides comprehensive technical reference for all I2PTunnel configuration properties. Properties are shown in split format (without `tunnel.N.` prefix). For monolithic format, prefix all properties with `tunnel.N.` where N is the tunnel number.

**Important**: Properties described as `tunnel.N.option.i2cp.*` are implemented in I2PTunnel and are **NOT** supported via other interfaces such as I2CP protocol or SAM API.

### Basic Properties

#### tunnel.N.description (description)
- **Type**: String
- **Context**: All tunnels
- **Description**: Human-readable tunnel description for UI display
- **Example**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (name)
- **Type**: String
- **Context**: All tunnels
- **Required**: Yes
- **Description**: Unique tunnel identifier and display name
- **Example**: `name=I2P HTTP Proxy`

#### tunnel.N.type (type)
- **Type**: Enum
- **Context**: All tunnels
- **Required**: Yes
- **Values**:
  - `client` - Generic client tunnel
  - `httpclient` - HTTP proxy client
  - `ircclient` - IRC client tunnel
  - `socksirctunnel` - SOCKS IRC proxy
  - `sockstunnel` - SOCKS proxy (version 4, 4a, 5)
  - `connectclient` - CONNECT proxy client
  - `streamrclient` - Streamr client
  - `server` - Generic server tunnel
  - `httpserver` - HTTP server tunnel
  - `ircserver` - IRC server tunnel
  - `httpbidirserver` - Bidirectional HTTP server
  - `streamrserver` - Streamr server

#### tunnel.N.interface (interface)
- **Type**: String (IP address or hostname)
- **Context**: Client tunnels only
- **Default**: 127.0.0.1
- **Description**: Local interface to bind for incoming connections
- **Security Note**: Binding to 0.0.0.0 allows remote connections
- **Example**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)
- **Type**: Integer
- **Context**: Client tunnels only
- **Range**: 1-65535
- **Description**: Local port to listen on for client connections
- **Example**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)
- **Type**: String (IP address or hostname)
- **Context**: Server tunnels only
- **Description**: Local server to forward connections to
- **Example**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)
- **Type**: Integer
- **Context**: Server tunnels only
- **Range**: 1-65535
- **Description**: Port on targetHost to connect to
- **Example**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)
- **Type**: String (comma or space-separated destinations)
- **Context**: Client tunnels only
- **Format**: `destination[:port][,destination[:port]]`
- **Description**: I2P destination(s) to connect to
- **Examples**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)
- **Type**: String (IP address or hostname)
- **Default**: 127.0.0.1
- **Description**: I2P router I2CP interface address
- **Note**: Ignored when running in router context
- **Example**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)
- **Type**: Integer
- **Default**: 7654
- **Range**: 1-65535
- **Description**: I2P router I2CP port
- **Note**: Ignored when running in router context
- **Example**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)
- **Type**: Boolean
- **Default**: true
- **Description**: Whether to start tunnel when I2PTunnel loads
- **Example**: `startOnLoad=true`

### Proxy Configuration

#### tunnel.N.proxyList (proxyList)
- **Type**: String (comma or space-separated hostnames)
- **Context**: HTTP and SOCKS proxies only
- **Description**: List of outproxy hosts
- **Example**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Server Configuration

#### tunnel.N.privKeyFile (privKeyFile)
- **Type**: String (file path)
- **Context**: Servers and persistent client tunnels
- **Description**: File containing persistent destination private keys
- **Path**: Absolute or relative to I2P config directory
- **Example**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)
- **Type**: String (hostname)
- **Context**: HTTP servers only
- **Default**: Base32 hostname of destination
- **Description**: Host header value passed to local server
- **Example**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)
- **Type**: String (hostname)
- **Context**: HTTP servers only
- **Description**: Virtual host override for specific incoming port
- **Use Case**: Host multiple sites on different ports
- **Example**: `spoofedHost.8080=site1.example.i2p`

### Client-Specific Options

#### tunnel.N.sharedClient (sharedClient)
- **Type**: Boolean
- **Context**: Client tunnels only
- **Default**: false
- **Description**: Whether multiple clients can share this tunnel
- **Example**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)
- **Type**: Boolean
- **Context**: Client tunnels only
- **Default**: false
- **Description**: Store and reuse destination keys across restarts
- **Conflict**: Mutually exclusive with `i2cp.newDestOnResume=true`
- **Example**: `option.persistentClientKey=true`

### I2CP Options (I2PTunnel Implementation)

**Important**: These properties are prefixed with `option.i2cp.` but are **implemented in I2PTunnel**, not in the I2CP protocol layer. They are not available via I2CP or SAM APIs.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)
- **Type**: Boolean
- **Context**: Client tunnels only
- **Default**: false
- **Description**: Delay tunnel creation until first connection
- **Use Case**: Save resources for rarely-used tunnels
- **Example**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)
- **Type**: Boolean
- **Context**: Client tunnels only
- **Default**: false
- **Requires**: `i2cp.closeOnIdle=true`
- **Conflict**: Mutually exclusive with `persistentClientKey=true`
- **Description**: Create new destination after idle timeout
- **Example**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)
- **Type**: String (base64-encoded key)
- **Context**: Server tunnels only
- **Description**: Persistent private leaseset encryption key
- **Use Case**: Maintain consistent encrypted leaseset across restarts
- **Example**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)
- **Type**: String (sigtype:base64)
- **Context**: Server tunnels only
- **Format**: `sigtype:base64key`
- **Description**: Persistent leaseset signing private key
- **Example**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Server-Specific Options

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)
- **Type**: Boolean
- **Context**: Server tunnels only
- **Default**: false
- **Description**: Use unique local IP per remote I2P destination
- **Use Case**: Track client IPs in server logs
- **Security Note**: May reduce anonymity
- **Example**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)
- **Type**: String (hostname:port)
- **Context**: Server tunnels only
- **Description**: Override targetHost/targetPort for incoming port NNNN
- **Use Case**: Port-based routing to different local services
- **Example**: `option.targetForPort.8080=localhost:8080`

### Thread Pool Configuration

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)
- **Type**: Boolean
- **Context**: Server tunnels only
- **Default**: true
- **Description**: Use thread pool for connection handling
- **Note**: Always false for standard servers (ignored)
- **Example**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)
- **Type**: Integer
- **Context**: Server tunnels only
- **Default**: 65
- **Description**: Maximum thread pool size
- **Note**: Ignored for standard servers
- **Example**: `option.i2ptunnel.blockingHandlerCount=100`

### HTTP Client Options

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: false
- **Description**: Allow SSL connections to .i2p addresses
- **Example**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: false
- **Description**: Disable address helper links in proxy responses
- **Example**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)
- **Type**: String (comma or space-separated URLs)
- **Context**: HTTP clients only
- **Description**: Jump server URLs for hostname resolution
- **Example**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: false
- **Description**: Pass Accept-* headers (except Accept and Accept-Encoding)
- **Example**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: false
- **Description**: Pass Referer headers through proxy
- **Privacy Note**: May leak information
- **Example**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: false
- **Description**: Pass User-Agent headers through proxy
- **Privacy Note**: May leak browser information
- **Example**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: false
- **Description**: Pass Via headers through proxy
- **Example**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)
- **Type**: String (comma or space-separated destinations)
- **Context**: HTTP clients only
- **Description**: In-network SSL outproxies for HTTPS
- **Example**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: true
- **Description**: Use registered local outproxy plugins
- **Example**: `option.i2ptunnel.useLocalOutproxy=true`

### HTTP Client Authentication

#### tunnel.N.option.proxyAuth (option.proxyAuth)
- **Type**: Enum
- **Context**: HTTP clients only
- **Default**: false
- **Values**: `true`, `false`, `basic`, `digest`
- **Description**: Require local authentication for proxy access
- **Note**: `true` is equivalent to `basic`
- **Example**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)
- **Type**: String (32 character lowercase hex)
- **Context**: HTTP clients only
- **Requires**: `proxyAuth=basic` or `proxyAuth=digest`
- **Description**: MD5 hash of password for user USER
- **Deprecation**: Use SHA-256 instead (0.9.56+)
- **Example**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)
- **Type**: String (64 character lowercase hex)
- **Context**: HTTP clients only
- **Requires**: `proxyAuth=digest`
- **Since**: Version 0.9.56
- **Standard**: RFC 7616
- **Description**: SHA-256 hash of password for user USER
- **Example**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Outproxy Authentication

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)
- **Type**: Boolean
- **Context**: HTTP clients only
- **Default**: false
- **Description**: Send authentication to outproxy
- **Example**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)
- **Type**: String
- **Context**: HTTP clients only
- **Requires**: `outproxyAuth=true`
- **Description**: Username for outproxy authentication
- **Example**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)
- **Type**: String
- **Context**: HTTP clients only
- **Requires**: `outproxyAuth=true`
- **Description**: Password for outproxy authentication
- **Security**: Stored in plaintext
- **Example**: `option.outproxyPassword=secret`

### SOCKS Client Options

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)
- **Type**: String (comma or space-separated destinations)
- **Context**: SOCKS clients only
- **Description**: In-network outproxies for unspecified ports
- **Example**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)
- **Type**: String (comma or space-separated destinations)
- **Context**: SOCKS clients only
- **Description**: In-network outproxies for port NNNN specifically
- **Example**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)
- **Type**: Enum
- **Context**: SOCKS clients only
- **Default**: socks
- **Since**: Version 0.9.57
- **Values**: `socks`, `connect` (HTTPS)
- **Description**: Type of configured outproxy
- **Example**: `option.outproxyType=connect`

### HTTP Server Options

#### tunnel.N.option.maxPosts (option.maxPosts)
- **Type**: Integer
- **Context**: HTTP servers only
- **Default**: 0 (unlimited)
- **Description**: Max POSTs from one destination per postCheckTime
- **Example**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)
- **Type**: Integer
- **Context**: HTTP servers only
- **Default**: 0 (unlimited)
- **Description**: Max POSTs from all destinations per postCheckTime
- **Example**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)
- **Type**: Integer (seconds)
- **Context**: HTTP servers only
- **Default**: 300
- **Description**: Time window for checking POST limits
- **Example**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)
- **Type**: Integer (seconds)
- **Context**: HTTP servers only
- **Default**: 1800
- **Description**: Ban duration after maxPosts exceeded for single destination
- **Example**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)
- **Type**: Integer (seconds)
- **Context**: HTTP servers only
- **Default**: 600
- **Description**: Ban duration after maxTotalPosts exceeded
- **Example**: `option.postTotalBanTime=1200`

### HTTP Server Security Options

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)
- **Type**: Boolean
- **Context**: HTTP servers only
- **Default**: false
- **Description**: Reject connections apparently via an inproxy
- **Example**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)
- **Type**: Boolean
- **Context**: HTTP servers only
- **Default**: false
- **Since**: Version 0.9.25
- **Description**: Reject connections with Referer header
- **Example**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)
- **Type**: Boolean
- **Context**: HTTP servers only
- **Default**: false
- **Since**: Version 0.9.25
- **Requires**: `userAgentRejectList` property
- **Description**: Reject connections with matching User-Agent
- **Example**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)
- **Type**: String (comma-separated match strings)
- **Context**: HTTP servers only
- **Since**: Version 0.9.25
- **Case**: Case-sensitive matching
- **Special**: "none" (since 0.9.33) matches empty User-Agent
- **Description**: List of User-Agent patterns to reject
- **Example**: `option.userAgentRejectList=Mozilla,Opera,none`

### IRC Server Options

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)
- **Type**: String (hostname pattern)
- **Context**: IRC servers only
- **Default**: `%f.b32.i2p`
- **Tokens**:
  - `%f` = Full base32 destination hash
  - `%c` = Cloaked destination hash (see cloakKey)
- **Description**: Hostname format sent to IRC server
- **Example**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)
- **Type**: String (passphrase)
- **Context**: IRC servers only
- **Default**: Random per session
- **Restrictions**: No quotes or spaces
- **Description**: Passphrase for consistent hostname cloaking
- **Use Case**: Persistent user tracking across restarts/servers
- **Example**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)
- **Type**: Enum
- **Context**: IRC servers only
- **Default**: user
- **Values**: `user`, `webirc`
- **Description**: Authentication method for IRC server
- **Example**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)
- **Type**: String (password)
- **Context**: IRC servers only
- **Requires**: `method=webirc`
- **Restrictions**: No quotes or spaces
- **Description**: Password for WEBIRC protocol authentication
- **Example**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)
- **Type**: String (IP address)
- **Context**: IRC servers only
- **Requires**: `method=webirc`
- **Description**: Spoofed IP address for WEBIRC protocol
- **Example**: `option.ircserver.webircSpoofIP=10.0.0.1`

### SSL/TLS Configuration

#### tunnel.N.option.useSSL (option.useSSL)
- **Type**: Boolean
- **Default**: false
- **Context**: All tunnels
- **Behavior**:
  - **Servers**: Use SSL for connections to local server
  - **Clients**: Require SSL from local clients
- **Example**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)
- **Type**: String (file path)
- **Context**: Client tunnels only
- **Default**: `i2ptunnel-(random).ks`
- **Path**: Relative to `$(I2P_CONFIG_DIR)/keystore/` if not absolute
- **Auto-generated**: Created if doesn't exist
- **Description**: Keystore file containing SSL private key
- **Example**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)
- **Type**: String (password)
- **Context**: Client tunnels only
- **Default**: changeit
- **Auto-generated**: Random password if new keystore created
- **Description**: Password for SSL keystore
- **Example**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)
- **Type**: String (alias)
- **Context**: Client tunnels only
- **Auto-generated**: Created if new key generated
- **Description**: Alias for private key in keystore
- **Example**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)
- **Type**: String (password)
- **Context**: Client tunnels only
- **Auto-generated**: Random password if new key created
- **Description**: Password for private key in keystore
- **Example**: `option.keyPassword=keypass123`

### Generic I2CP and Streaming Options

All `tunnel.N.option.*` properties (not specifically documented above) are passed through to the I2CP interface and streaming library with the `tunnel.N.option.` prefix stripped.

**Important**: These are separate from I2PTunnel-specific options. Refer to:
- [I2CP Specification](/docs/specs/i2cp/)
- [Streaming Library Specification](/docs/specs/streaming/)

Example streaming options:
```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```

### Complete Tunnel Example

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```

---

## Version History and Feature Timeline

### Version 0.9.10 (2013)
**Feature**: Empty value support in configuration files
- Keys with empty values (`key=`) now supported
- Previously ignored or caused parsing errors

### Version 0.9.18 (2015)
**Feature**: Logger flush interval configuration
- Property: `logger.flushInterval` (default 29 seconds)
- Reduces disk I/O while maintaining acceptable log latency

### Version 0.9.23 (November 2015)
**Major Change**: Java 7 minimum requirement
- Java 6 support ended
- Required for continued security updates

### Version 0.9.25 (2015)
**Features**: HTTP server security options
- `tunnel.N.option.rejectReferer` - Reject connections with Referer header
- `tunnel.N.option.rejectUserAgents` - Reject specific User-Agent headers
- `tunnel.N.option.userAgentRejectList` - User-Agent patterns to reject
- **Use Case**: Mitigate crawlers and unwanted clients

### Version 0.9.33 (January 2018)
**Feature**: Enhanced User-Agent filtering
- `userAgentRejectList` string "none" matches empty User-Agent
- Additional bug fixes for i2psnark, i2ptunnel, streaming, SusiMail

### Version 0.9.41 (2019)
**Deprecation**: BOB Protocol removed from Android
- Android users must migrate to SAM or I2CP

### Version 0.9.42 (August 2019)
**Major Change**: Configuration file splitting
- `clients.config` split into `clients.config.d/` directory structure
- `i2ptunnel.config` split into `i2ptunnel.config.d/` directory structure
- Automatic migration on first run after upgrade
- Enables modular packaging and plugin management
- Legacy monolithic format still supported

**Additional Features**:
- SSU performance improvements
- Cross-network prevention (Proposal 147)
- Initial encryption type support

### Version 0.9.56 (2021)
**Features**: Security and logging improvements
- `logger.gzip` - Gzip compression for rotated logs (default: false)
- `logger.minGzipSize` - Minimum size for compression (default: 65536 bytes)
- `tunnel.N.option.proxy.auth.USER.sha256` - SHA-256 digest authentication (RFC 7616)
- **Security**: SHA-256 replaces MD5 for digest authentication

### Version 0.9.57 (January 2023)
**Feature**: SOCKS outproxy type configuration
- `tunnel.N.option.outproxyType` - Select outproxy type (socks|connect)
- Default: socks
- HTTPS CONNECT support for HTTPS outproxies

### Version 2.6.0 (July 2024)
**Breaking Change**: I2P-over-Tor blocked
- Connections from Tor exit node IP addresses now rejected
- **Reason**: Degrades I2P performance, wastes Tor exit resources
- **Impact**: Users accessing I2P through Tor exit nodes will be blocked
- Non-exit relays and Tor clients unaffected

### Version 2.10.0 (September 2025 - Current)
**Major Features**:
- **Post-quantum cryptography** available (opt-in via Hidden Service Manager)
- **UDP tracker support** for I2PSnark to reduce tracker load
- **Hidden Mode stability** improvements to reduce RouterInfo depletion
- Network improvements for congested routers
- Enhanced UPnP/NAT traversal
- NetDB improvements with aggressive leaseset removal
- Observability reductions for router events

**Configuration**: No new configuration properties added

**Critical Upcoming Change**: Next release (likely 2.11.0 or 3.0.0) will require Java 17 or later

---

## Deprecations and Breaking Changes

### Critical Deprecations

#### I2P-over-Tor Access (Version 2.6.0+)
- **Status**: BLOCKED since July 2024
- **Impact**: Connections from Tor exit node IPs rejected
- **Reason**: Degrades I2P network performance without providing anonymity benefits
- **Affects**: Only Tor exit nodes, not relays or regular Tor clients
- **Alternative**: Use I2P or Tor separately, not combined

#### MD5 Digest Authentication
- **Status**: Deprecated (use SHA-256)
- **Property**: `tunnel.N.option.proxy.auth.USER.md5`
- **Reason**: MD5 cryptographically broken
- **Replacement**: `tunnel.N.option.proxy.auth.USER.sha256` (since 0.9.56)
- **Timeline**: MD5 still supported but discouraged

### Configuration Architecture Changes

#### Monolithic Configuration Files (Version 0.9.42+)
- **Affected**: `clients.config`, `i2ptunnel.config`
- **Status**: Deprecated in favor of split directory structure
- **Migration**: Automatic on first run after 0.9.42 upgrade
- **Compatibility**: Legacy format still works (backward compatible)
- **Recommendation**: Use split format for new configurations

### Java Version Requirements

#### Java 6 Support
- **Ended**: Version 0.9.23 (November 2015)
- **Minimum**: Java 7 required since 0.9.23

#### Java 17 Requirement (Upcoming)
- **Status**: CRITICAL UPCOMING CHANGE
- **Target**: Next major release after 2.10.0 (likely 2.11.0 or 3.0.0)
- **Current Minimum**: Java 8
- **Action Required**: Prepare for Java 17 migration
- **Timeline**: To be announced with release notes

### Removed Features

#### BOB Protocol (Android)
- **Removed**: Version 0.9.41
- **Platform**: Android only
- **Alternative**: SAM or I2CP protocols
- **Desktop**: BOB still available on desktop platforms

### Recommended Migrations

1. **Authentication**: Migrate from MD5 to SHA-256 digest authentication
2. **Configuration Format**: Migrate to split directory structure for clients and tunnels
3. **Java Runtime**: Plan for Java 17 upgrade before next major release
4. **Tor Integration**: Do not route I2P through Tor exit nodes

---

## References

### Official Documentation

- [I2P Configuration Specification](/docs/specs/configuration/) - Official configuration file format specification
- [I2P Plugin Specification](/docs/specs/plugin/) - Plugin configuration and packaging
- [I2P Common Structures - Type Mapping](/docs/specs/common-structures/#type-mapping) - Protocol data serialization format
- [Java Properties Format](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Base format specification

### Source Code

- [I2P Java Router Repository](https://github.com/i2p/i2p.i2p) - GitHub mirror
- [I2P Developers Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p) - Official I2P source repository
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Configuration file I/O implementation

### Community Resources

- [I2P Forum](https://i2pforum.net/) - Active community discussions and support
- [I2P Website](/) - Official project website

### API Documentation

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - API documentation for configuration file methods

### Specification Status

- **Last Specification Update**: January 2023 (Version 0.9.57)
- **Current I2P Version**: 2.10.0 (September 2025)
- **Technical Accuracy**: Specification remains accurate through 2.10.0 (no breaking changes)
- **Maintenance**: Living document updated when configuration format modified
