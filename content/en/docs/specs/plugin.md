---
title: "Plugin Package Format"
description: ".xpi2p / .su3 packaging rules for I2P plugins"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
aliases:
  - /spec/plugin/
---

## Overview

I2P plugins are signed archives that extend router functionality. They ship as `.xpi2p` or `.su3` files, install to `~/.i2p/plugins/<name>/` (or `%APPDIR%\I2P\plugins\<name>\` on Windows), and run with full router permissions without sandboxing.

### Supported Plugin Types

- Console webapps
- New eepsites with cgi-bin, webapps
- Console themes
- Console translations
- Java programs (in-process or separate JVM)
- Shell scripts and native binaries

### Security Model

**CRITICAL:** Plugins run in the same JVM with identical permissions as the I2P router. They have unrestricted access to:
- File system (read and write)
- Router APIs and internal state
- Network connections
- External program execution

Plugins should be treated as fully trusted code. Users must verify plugin sources and signatures before installation.

---

## File Formats

### SU3 Format (Strongly Recommended)

**Status:** Active, preferred format since I2P 0.9.15 (September 2014)

The `.su3` format provides:
- **RSA-4096 signing keys** (vs. DSA-1024 in xpi2p)
- Signature stored in file header
- Magic number: `I2Psu3`
- Better forward compatibility

**Structure:**
```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```

### XPI2P Format (Legacy, Deprecated)

**Status:** Supported for backwards compatibility, not recommended for new plugins

The `.xpi2p` format uses older cryptographic signatures:
- **DSA-1024 signatures** (obsolete per NIST-800-57)
- 40-byte DSA signature prepended to ZIP
- Requires `key` field in plugin.config

**Structure:**
```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```

**Migration Path:** When migrating from xpi2p to su3, provide both `updateURL` and `updateURL.su3` during transition. Modern routers (0.9.15+) automatically prioritize SU3.

---

## Archive Layout and plugin.config

### Required Files

**plugin.config** - Standard I2P configuration file with key-value pairs

### Required Properties

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>

**Version Format Examples:**
- `1.2.3`
- `1.2.3-4`
- `2.0.0-beta.1`

Valid separators: `.` (dot), `-` (dash), `_` (underscore)

### Optional Metadata Properties

#### Display Information
- `date` - Release date (Java long timestamp)
- `author` - Developer name (`user@mail.i2p` recommended)
- `description` - English description
- `description_xx` - Localized description (xx = language code)
- `websiteURL` - Plugin homepage (`http://foo.i2p/`)
- `license` - License identifier (e.g., "Apache-2.0", "GPL-3.0")

#### Update Configuration
- `updateURL` - XPI2P update location (legacy)
- `updateURL.su3` - SU3 update location (preferred)
- `min-i2p-version` - Minimum I2P version required
- `max-i2p-version` - Maximum compatible I2P version
- `min-java-version` - Minimum Java version (e.g., `1.7`, `17`)
- `min-jetty-version` - Minimum Jetty version (use `6` for Jetty 6+)
- `max-jetty-version` - Maximum Jetty version (use `5.99999` for Jetty 5)

#### Installation Behavior
- `dont-start-at-install` - Default `false`. If `true`, requires manual start
- `router-restart-required` - Default `false`. Informs user restart needed after update
- `update-only` - Default `false`. Fails if plugin not already installed
- `install-only` - Default `false`. Fails if plugin already exists
- `min-installed-version` - Minimum version required for update
- `max-installed-version` - Maximum version that can be updated
- `disableStop` - Default `false`. Hides stop button if `true`

#### Console Integration
- `consoleLinkName` - Text for console summary bar link
- `consoleLinkName_xx` - Localized link text (xx = language code)
- `consoleLinkURL` - Link destination (e.g., `/appname/index.jsp`)
- `consoleLinkTooltip` - Hover text (supported since 0.7.12-6)
- `consoleLinkTooltip_xx` - Localized tooltip
- `console-icon` - Path to 32x32 icon (supported since 0.9.20)
- `icon-code` - Base64-encoded 32x32 PNG for plugins without web resources (since 0.9.25)

#### Platform Requirements (Display Only)
- `required-platform-OS` - Operating system requirement (not enforced)
- `other-requirements` - Additional requirements (e.g., "Python 3.8+")

#### Dependency Management (Unimplemented)
- `depends` - Comma-separated plugin dependencies
- `depends-version` - Version requirements for dependencies
- `langs` - Language pack contents
- `type` - Plugin type (app/theme/locale/webapp)

### Update URL Variable Substitution

**Feature Status:** Available since I2P 1.7.0 (0.9.53)

Both `updateURL` and `updateURL.su3` support platform-specific variables:

**Variables:**
- `$OS` - Operating system: `windows`, `linux`, `mac`
- `$ARCH` - Architecture: `386`, `amd64`, `arm64`

**Example:**
```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```

**Result on Windows AMD64:**
```
http://foo.i2p/downloads/foo-windows-amd64.su3
```

This enables single plugin.config files for platform-specific builds.

---

## Directory Structure

### Standard Layout

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```

### Directory Purposes

**console/locale/**
- JAR files with resource bundles for I2P base translations
- Plugin-specific translations should be in `console/webapps/*.war` or `lib/*.jar`

**console/themes/**
- Each subdirectory contains a complete console theme
- Automatically added to theme search path

**console/webapps/**
- `.war` files for console integration
- Started automatically unless disabled in `webapps.config`
- War name does not need to match plugin name

**eepsite/**
- Complete eepsite with own Jetty instance
- Requires `jetty.xml` configuration with variable substitution
- See zzzot and pebble plugin examples

**lib/**
- Plugin JAR libraries
- Specify in classpath via `clients.config` or `webapps.config`

---

## Webapp Configuration

### webapps.config Format

Standard I2P configuration file controlling webapp behavior.

**Syntax:**
```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```

**Important Notes:**
- Prior to router 0.7.12-9, use `plugin.warname.startOnLoad` for compatibility
- Prior to API 0.9.53, classpath only worked if warname matched plugin name
- As of 0.9.53+, classpath works for any webapp name

### Webapp Best Practices

1. **ServletContextListener Implementation**
   - Implement `javax.servlet.ServletContextListener` for cleanup
   - Or override `destroy()` in servlet
   - Ensures proper shutdown during updates and router stop

2. **Library Management**
   - Place shared JARs in `lib/`, not inside WAR
   - Reference via `webapps.config` classpath
   - Enables separate install/update plugins

3. **Avoid Conflicting Libraries**
   - Never bundle Jetty, Tomcat, or servlet JARs
   - Never bundle JARs from standard I2P installation
   - Check classpath section for standard libraries

4. **Compilation Requirements**
   - Do not include `.java` or `.jsp` source files
   - Pre-compile all JSPs to avoid startup delays
   - Cannot assume Java/JSP compiler availability

5. **Servlet API Compatibility**
   - I2P supports Servlet 3.0 (since 0.9.30)
   - **Annotation scanning NOT supported** (@WebContent)
   - Must provide traditional `web.xml` deployment descriptor

6. **Jetty Version**
   - Current: Jetty 9 (I2P 0.9.30+)
   - Use `net.i2p.jetty.JettyStart` for abstraction
   - Protects against Jetty API changes

---

## Client Configuration

### clients.config Format

Defines clients (services) started with plugin.

**Basic Client:**
```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```

**Client with Stop/Uninstall:**
```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```

### Property Reference

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>

### Variable Substitution

The following variables are replaced in `args`, `stopargs`, `uninstallargs`, and `classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>

### Managed vs. Unmanaged Clients

**Managed Clients (Recommended, since 0.9.4):**
- Instantiated by ClientAppManager
- Maintains reference and state tracking
- Easier lifecycle management
- Better memory management

**Unmanaged Clients:**
- Started by router, no state tracking
- Must handle multiple start/stop calls gracefully
- Use static state or PID files for coordination
- Called at router shutdown (as of 0.7.12-3)

### ShellService (since 0.9.53 / 1.7.0)

Generalized solution for running external programs with automatic state tracking.

**Features:**
- Handles process lifecycle
- Communicates with ClientAppManager
- Automatic PID management
- Cross-platform support

**Usage:**
```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```

For platform-specific scripts:
```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```

**Alternative (Legacy):** Write Java wrapper checking OS type, call `ShellCommand` with appropriate `.bat` or `.sh` file.

---

## Installation Process

### User Installation Flow

1. User pastes plugin URL into Router Console Plugin Configuration Page (`/configplugins`)
2. Router downloads plugin file
3. Signature verification (fails if key unknown and strict mode enabled)
4. ZIP integrity check
5. Extract and parse `plugin.config`
6. Version compatibility verification (`min-i2p-version`, `min-java-version`, etc.)
7. Webapp name conflict detection
8. Stop existing plugin if update
9. Directory validation (must be under `plugins/`)
10. Extract all files to plugin directory
11. Update `plugins.config`
12. Start plugin (unless `dont-start-at-install=true`)

### Security and Trust

**Key Management:**
- First-key-seen trust model for new signers
- Only jrandom and zzz keys pre-bundled
- As of 0.9.14.1, unknown keys rejected by default
- Advanced property can override for development

**Installation Restrictions:**
- Archives must unpack to plugin directory only
- Installer refuses paths outside `plugins/`
- Plugins can access files elsewhere after installation
- No sandboxing or privilege isolation

---

## Update Mechanism

### Update Check Process

1. Router reads `updateURL.su3` (preferred) or `updateURL` from plugin.config
2. HTTP HEAD or partial GET request to fetch bytes 41-56
3. Extract version string from remote file
4. Compare with installed version using VersionComparator
5. If newer, prompt user or auto-download (based on settings)
6. Stop plugin
7. Install update
8. Start plugin (unless user preference changed)

### Version Comparison

Versions parsed as dot/dash/underscore-separated components:
- `1.2.3` < `1.2.4`
- `1.2.3` < `1.2.3-1`
- `2.0.0` > `1.9.9`

**Maximum length:** 16 bytes (must match SUD/SU3 header)

### Update Best Practices

1. Always increment version for releases
2. Test update path from previous version
3. Consider `router-restart-required` for major changes
4. Provide both `updateURL` and `updateURL.su3` during migration
5. Use build number suffix for testing (`1.2.3-456`)

---

## Classpath and Standard Libraries

### Always Available in Classpath

The following JARs from `$I2P/lib` are always in classpath for I2P 0.9.30+:

| JAR | Contents | Plugin Usage |
|-----|----------|--------------|
| `i2p.jar` | Core API | Required for all plugins |
| `mstreaming.jar` | Streaming API | Most plugins need |
| `streaming.jar` | Streaming implementation | Most plugins need |
| `i2ptunnel.jar` | I2PTunnel | HTTP/server plugins |
| `router.jar` | Router internals | Rarely needed, avoid if possible |
| `javax.servlet.jar` | Servlet 3.1, JSP 2.3 API | Plugins with servlets/JSPs |
| `jasper-runtime.jar` | Jasper compiler/runtime | Plugins with JSPs |
| `commons-el.jar` | EL 3.0 API | JSPs using expression language |
| `jetty-i2p.jar` | Jetty utilities | Plugins starting Jetty |
| `org.mortbay.jetty.jar` | Jetty 9 base | Custom Jetty instances |
| `sam.jar` | SAM API | Rarely needed |
| `addressbook.jar` | Subscription/blockfile | Use NamingService instead |
| `routerconsole.jar` | Console libraries | Not public API, avoid |
| `jbigi.jar` | Native crypto | Plugins should not need |
| `systray.jar` | URL launcher | Rarely needed |
| `wrapper.jar` | Service wrapper | Plugins should not need |

### Special Notes

**commons-logging.jar:**
- Empty since 0.9.30
- Prior to 0.9.30: Apache Tomcat JULI
- Prior to 0.9.24: Commons Logging + JULI
- Prior to 0.9: Commons Logging only

**jasper-compiler.jar:**
- Empty since Jetty 6 (0.9)

**systray4j.jar:**
- Removed in 0.9.26

### Not in Classpath (Must Specify)

| JAR | Contents | Usage |
|-----|----------|-------|
| `jstl.jar` | Standard Taglib | JSP tag libraries |
| `standard.jar` | Standard Taglib | JSP tag libraries |

### Classpath Specification

**In clients.config:**
```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```

**In webapps.config:**
```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```

**Important:** As of 0.7.13-3, classpaths are thread-specific, not JVM-wide. Specify complete classpath for each client.

---

## Java Version Requirements

### Current Requirements (October 2025)

**I2P 2.10.0 and earlier:**
- Minimum: Java 7 (required since 0.9.24, January 2016)
- Recommended: Java 8 or higher

**I2P 2.11.0 and later (UPCOMING):**
- **Minimum: Java 17+** (announced in 2.9.0 release notes)
- Two-release warning given (2.9.0 → 2.10.0 → 2.11.0)

### Plugin Compatibility Strategy

**For maximum compatibility (through I2P 2.10.x):**
```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```

**For Java 8+ features:**
```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```

**For Java 11+ features:**
```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```

**Preparing for 2.11.0+:**
```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```

### Compilation Best Practices

**When compiling with newer JDK for older target:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```

This prevents using APIs not available in target Java version.

---

## Pack200 Compression - OBSOLETE

### Critical Update: Do Not Use Pack200

**Status:** DEPRECATED AND REMOVED

The original specification strongly recommended Pack200 compression for 60-65% size reduction. **This is no longer valid.**

**Timeline:**
- **JEP 336:** Pack200 deprecated in Java 11 (September 2018)
- **JEP 367:** Pack200 removed in Java 14 (March 2020)

**Official I2P Updates Specification states:**
> "Jar and war files in the zip are no longer compressed with pack200 as documented above for 'su2' files, because recent Java runtimes no longer support it."

**What to Do:**

1. **Remove pack200 from build processes immediately**
2. **Use standard ZIP compression**
3. **Consider alternatives:**
   - ProGuard/R8 for code shrinking
   - UPX for native binaries
   - Modern compression algorithms (zstd, brotli) if custom unpacker provided

**For Existing Plugins:**
- Old routers (0.7.11-5 through Java 10) can still unpack pack200
- New routers (Java 11+) cannot unpack pack200
- Re-release plugins without pack200 compression

---

## Signing Keys and Security

### Key Generation (SU3 Format)

Use `makeplugin.sh` script from i2p.scripts repository:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```

**Key Details:**
- Algorithm: RSA_SHA512_4096
- Format: X.509 certificate
- Storage: Java keystore format

### Signing Plugins

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```

### Key Management Best Practices

1. **Generate once, safeguard forever**
   - Routers reject duplicate keynames with different keys
   - Routers reject duplicate keys with different keynames
   - Updates rejected if key/name mismatch

2. **Secure storage**
   - Backup keystore securely
   - Use strong passphrase
   - Never commit to version control

3. **Key rotation**
   - Not supported by current architecture
   - Plan for long-term key usage
   - Consider multi-signature schemes for team development

### Legacy DSA Signing (XPI2P)

**Status:** Functional but obsolete

DSA-1024 signatures used by xpi2p format:
- 40-byte signature
- 172 base64 character public key
- NIST-800-57 recommends (L=2048, N=224) minimum
- I2P uses weaker (L=1024, N=160)

**Recommendation:** Use SU3 with RSA-4096 instead.

---

## Plugin Development Guidelines

### Essential Best Practices

1. **Documentation**
   - Provide clear README with installation instructions
   - Document configuration options and defaults
   - Include changelog with each release
   - Specify required I2P/Java versions

2. **Size Optimization**
   - Include only necessary files
   - Never bundle router JARs
   - Separate install vs. update packages (libraries in lib/)
   - ~~Use Pack200 compression~~ **OBSOLETE - Use standard ZIP**

3. **Configuration**
   - Never modify `plugin.config` at runtime
   - Use separate config file for runtime settings
   - Document required router settings (SAM ports, tunnels, etc.)
   - Respect user's existing configuration

4. **Resource Usage**
   - Avoid aggressive default bandwidth consumption
   - Implement reasonable CPU usage limits
   - Clean up resources on shutdown
   - Use daemon threads where appropriate

5. **Testing**
   - Test install/upgrade/uninstall on all platforms
   - Test updates from previous version
   - Verify webapp stop/restart during updates
   - Test with minimum supported I2P version

6. **File System**
   - Never write to `$I2P` (may be read-only)
   - Write runtime data to `$PLUGIN` or `$CONFIG`
   - Use `I2PAppContext` for directory discovery
   - Do not assume `$CWD` location

7. **Compatibility**
   - Do not duplicate standard I2P classes
   - Extend classes if necessary, don't replace
   - Check `min-i2p-version`, `min-jetty-version` in plugin.config
   - Test with older I2P versions if supporting them

8. **Shutdown Handling**
   - Implement proper `stopargs` in clients.config
   - Register shutdown hooks: `I2PAppContext.addShutdownTask()`
   - Handle multiple start/stop calls gracefully
   - Set all threads to daemon mode

9. **Security**
   - Validate all external input
   - Never call `System.exit()`
   - Respect user privacy
   - Follow secure coding practices

10. **Licensing**
    - Clearly specify plugin license
    - Respect licenses of bundled libraries
    - Include required attribution
    - Provide source code access if required

### Advanced Considerations

**Timezone Handling:**
- Router sets JVM timezone to UTC
- User's actual timezone: `I2PAppContext` property `i2p.systemTimeZone`

**Directory Discovery:**
```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```

**Version Numbering:**
- Use semantic versioning (major.minor.patch)
- Add build number for testing (1.2.3-456)
- Ensure monotonic increase for updates

**Router Class Access:**
- Generally avoid `router.jar` dependencies
- Use public APIs in `i2p.jar` instead
- Future I2P may restrict router class access

**JVM Crash Prevention (Historical):**
- Fixed in 0.7.13-3
- Use class loaders properly
- Avoid updating JARs in running plugin
- Design for restart-on-update if necessary

---

## Eepsite Plugins

### Overview

Plugins can provide complete eepsites with own Jetty and I2PTunnel instances.

### Architecture

**Do not attempt to:**
- Install into existing eepsite
- Merge with router's default eepsite
- Assume single eepsite availability

**Instead:**
- Start new I2PTunnel instance (via CLI approach)
- Start new Jetty instance
- Configure both in `clients.config`

### Example Structure

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```

### Variable Substitution in jetty.xml

Use `$PLUGIN` variable for paths:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```

Router performs substitution during plugin start.

### Examples

Reference implementations:
- **zzzot plugin** - Torrent tracker
- **pebble plugin** - Blog platform

Both available at zzz's plugin page (I2P-internal).

---

## Console Integration

### Summary Bar Links

Add clickable link to router console summary bar:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```

Localized versions:
```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```

### Console Icons

**Image File (since 0.9.20):**
```properties
console-icon=/myicon.png
```

Path relative to `consoleLinkURL` if specified (since 0.9.53), otherwise relative to webapp name.

**Embedded Icon (since 0.9.25):**
```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```

Generate with:
```bash
base64 -w 0 icon-32x32.png
```

Or Java:
```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```

Requirements:
- 32x32 pixels
- PNG format
- Base64 encoded (no line breaks)

---

## Internationalization

### Translation Bundles

**For I2P Base Translations:**
- Place JARs in `console/locale/`
- Contain resource bundles for existing I2P apps
- Naming: `messages_xx.properties` (xx = language code)

**For Plugin-Specific Translations:**
- Include in `console/webapps/*.war`
- Or include in `lib/*.jar`
- Use standard Java ResourceBundle approach

### Localized Strings in plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```

Supported fields:
- `description_xx`
- `consoleLinkName_xx`
- `consoleLinkTooltip_xx`

### Console Theme Translation

Themes in `console/themes/` automatically added to theme search path.

---

## Platform-Specific Plugins

### Separate Packages Approach

Use different plugin names for each platform:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```

### Variable Substitution Approach

Single plugin.config with platform variables:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```

In clients.config:
```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```

### Runtime OS Detection

Java approach for conditional execution:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```

---

## Troubleshooting

### Common Issues

**Plugin Won't Start:**
1. Check I2P version compatibility (`min-i2p-version`)
2. Verify Java version (`min-java-version`)
3. Check router logs for errors
4. Verify all required JARs in classpath

**Webapp Not Accessible:**
1. Confirm `webapps.config` doesn't disable it
2. Check Jetty version compatibility (`min-jetty-version`)
3. Verify `web.xml` present (annotation scanning not supported)
4. Check for conflicting webapp names

**Update Fails:**
1. Verify version string increased
2. Check signature matches signing key
3. Ensure plugin name matches installed version
4. Review `update-only`/`install-only` settings

**External Program Won't Stop:**
1. Use ShellService for automatic lifecycle
2. Implement proper `stopargs` handling
3. Check PID file cleanup
4. Verify process termination

### Debug Logging

Enable debug logging in router:
```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```

Check logs:
```
~/.i2p/logs/log-router-0.txt
```

---

## Reference Information

### Official Specifications

- **Plugin Specification:** /docs/specs/plugin/
- **Configuration Format:** /docs/specs/configuration/
- **Update Specification:** /docs/specs/updates/
- **Cryptography:** /docs/specs/cryptography/

### I2P Version History

**Current Release:**
- **I2P 2.10.0** (September 8, 2025)

**Major Releases Since 0.9.53:**
- 2.10.0 (Sep 2025) - Java 17+ announcement
- 2.9.0 (Jun 2025) - Java 17+ warning
- 2.8.0 (Oct 2024) - Post-quantum crypto testing
- 2.6.0 (May 2024) - I2P-over-Tor blocking
- 2.4.0 (Dec 2023) - NetDB security improvements
- 2.2.0 (Mar 2023) - Congestion control
- 2.1.0 (Jan 2023) - Network improvements
- 2.0.0 (Nov 2022) - SSU2 transport protocol
- 1.7.0/0.9.53 (Feb 2022) - ShellService, variable substitution
- 0.9.15 (Sep 2014) - SU3 format introduced

**Version Numbering:**
- 0.9.x series: Through version 0.9.53
- 2.x series: Starting with 2.0.0 (SSU2 introduction)

### Developer Resources

**Source Code:**
- Main repository: https://i2pgit.org/I2P_Developers/i2p.i2p
- GitHub mirror: https://github.com/i2p/i2p.i2p

**Plugin Examples:**
- zzzot (BitTorrent tracker)
- pebble (Blog platform)
- i2p-bote (Serverless email)
- orchid (Tor client)
- seedless (Peer exchange)

**Build Tools:**
- makeplugin.sh - Key generation and signing
- Found in i2p.scripts repository
- Automates su3 creation and verification

### Community Support

**Forums:**
- I2P Forum: https://i2pforum.net/
- zzz.i2p: http://zzz.i2p/ (I2P-internal)

**IRC/Chat:**
- #i2p-dev on OFTC
- I2P IRC within network

**Mailing Lists:**
- i2p-dev@i2p2.de

---

## Appendix A: Complete plugin.config Example

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```

---

## Appendix B: Complete clients.config Example

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```

---

## Appendix C: Complete webapps.config Example

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```

---

## Appendix D: Migration Checklist (0.9.53 to 2.10.0)

### Required Changes

- [ ] **Remove Pack200 compression from build process**
  - Remove pack200 tasks from Ant/Maven/Gradle scripts
  - Re-release existing plugins without pack200

- [ ] **Review Java version requirements**
  - Consider requiring Java 11+ for new features
  - Plan for Java 17+ requirement in I2P 2.11.0
  - Update `min-java-version` in plugin.config

- [ ] **Update documentation**
  - Remove Pack200 references
  - Update Java version requirements
  - Update I2P version references (0.9.x → 2.x)

### Recommended Changes

- [ ] **Strengthen cryptographic signatures**
  - Migrate from XPI2P to SU3 if not already done
  - Use RSA-4096 keys for new plugins

- [ ] **Leverage new features (if using 0.9.53+)**
  - Use `$OS` / `$ARCH` variables for platform-specific updates
  - Use ShellService for external programs
  - Use improved webapp classpath (works for any warname)

- [ ] **Test compatibility**
  - Test on I2P 2.10.0
  - Verify with Java 8, 11, 17
  - Check on Windows, Linux, macOS

### Optional Enhancements

- [ ] Implement proper ServletContextListener
- [ ] Add localized descriptions
- [ ] Provide console icon
- [ ] Improve shutdown handling
- [ ] Add comprehensive logging
- [ ] Write automated tests

---

## Document Changelog

**Version 2.0 (October 2025):**
- Verified all content against I2P 2.10.0
- Added critical Pack200 deprecation warning
- Updated Java version requirements with 2.11.0 timeline
- Clarified DSA signature obsolescence
- Updated I2P version numbering (0.9.x → 2.x series)
- Confirmed all existing mechanisms remain valid
- Added troubleshooting section
- Expanded examples and best practices
- Verified all URLs and references

**Version 1.0 (January 2022):**
- Original specification for I2P 0.9.53
- Documented ShellService feature
- Documented variable substitution in update URLs
- Comprehensive coverage of plugin system
