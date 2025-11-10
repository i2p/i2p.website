---
title: "I2P Documentation Writing Guidelines"
description: "Maintain consistency, accuracy, and accessibility across I2P technical documentation"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Purpose:** Maintain consistency, accuracy, and accessibility across I2P technical documentation

---

## Core Principles

### 1. Verify Everything

**Never assume or guess.** All technical statements must be verified against:
- Current I2P source code (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master)
- Official API documentation (https://i2p.github.io/i2p.i2p/ 
- Configuration specifications [/docs/specs/](/docs/)
- Recent release notes [/releases/](/categories/release/)

**Example of proper verification:**
```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```

### 2. Clarity Over Brevity

Write for developers who may be encountering I2P for the first time. Explain concepts fully rather than assuming knowledge.

**Example:**
```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```

### 3. Accessibility First

Documentation must be accessible to developers on the clearnet (regular internet) even though I2P is a network overlay. Always provide clearnet-accessible alternatives to I2P-internal resources.

---

## Technical Accuracy

### API and Interface Documentation

**Always include:**
1. Full package names on first mention: `net.i2p.app.ClientApp`
2. Complete method signatures with return types
3. Parameter names and types
4. Required vs optional parameters

**Example:**
```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```

### Configuration Properties

When documenting configuration files:
1. Show exact property names
2. Specify file encoding (UTF-8 for I2P configs)
3. Provide complete examples
4. Document default values
5. Note version when properties were introduced/changed

**Example:**
```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```

### Constants and Enumerations

When documenting constants, use actual code names:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```

### Distinguish Between Similar Concepts

I2P has several overlapping systems. Always clarify which system you're documenting:

**Example:**
```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```

---

## Documentation URLs and References

### URL Accessibility Rules

1. **Primary references** should use clearnet-accessible URLs
2. **I2P-internal URLs** (.i2p domains) must include accessibility notes
3. **Always provide alternatives** when linking I2P-internal resources

**Template for I2P-internal URLs:**
```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```

### Recommended I2P Reference URLs

**Official specifications:**
- [Configuration](/docs/specs/configuration/)
- [Plugin](/docs/specs/plugin/)
- [Documentment Index](/docs/)

**API documentation (choose most current):**
- Most current: https://i2p.github.io/i2p.i2p/ (API 0.9.66 as of I2P 2.10.0)
- Clearnet mirror: https://eyedeekay.github.io/javadoc-i2p/

**Source code:**
- GitLab (official): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master
- GitHub mirror: https://github.com/i2p/i2p.i2p

### Link Format Standards

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```

---

## Version Tracking

### Document Metadata

Every technical document should include version metadata in frontmatter:

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```

**Field definitions:**
- `lastUpdated`: Year-month when document was last reviewed/updated
- `accurateFor`: I2P version the document was verified against
- `reviewStatus`: One of "draft", "needs-review", "verified", "outdated"

### Version References in Content

When mentioning versions:
1. Use **bold** for current version: "**version 2.10.0** (September 2025)"
2. Specify both version number and date for historical references
3. Note API version separately from I2P version when relevant

**Example:**
```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```

### Documenting Changes Over Time

For features that evolved:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```

### Deprecation Notices

If documenting deprecated features:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```

---

## Terminology Standards

### Official I2P Terms

Use these exact terms consistently:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>

### Managed Client Terminology

When documenting managed clients:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>

### Configuration Terminology

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>

### Package and Class Names

Always use fully qualified names on first mention, short names thereafter:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```

---

## Code Examples and Formatting

### Java Code Examples

Use proper syntax highlighting and complete examples:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```

**Code example requirements:**
1. Include comments explaining key lines
2. Show error handling where relevant
3. Use realistic variable names
4. Match I2P coding conventions (4-space indent)
5. Show imports if not obvious from context

### Configuration Examples

Show complete, valid configuration examples:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```

### Command Line Examples

Use `$` for user commands, `#` for root:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```

### Inline Code

Use backticks for:
- Method names: `startup()`
- Class names: `ClientApp`
- Property names: `clientApp.0.main`
- File names: `clients.config`
- Constants: `SVC_HTTP_PROXY`
- Package names: `net.i2p.app`

---

## Tone and Voice

### Professional but Accessible

Write for a technical audience without being condescending:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```

### Active Voice

Use active voice for clarity:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```

### Imperatives for Instructions

Use direct imperatives in procedural content:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```

### Avoid Unnecessary Jargon

Explain terms on first use:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```

### Punctuation Guidelines

1. **No em-dashes** - use regular dashes, commas, or semicolons instead
2. Use **Oxford comma** in lists: "console, i2ptunnel, and Jetty"
3. **Periods inside code blocks** only when grammatically necessary
4. **Serial lists** use semicolons when items contain commas

---

## Document Structure

### Standard Section Order

For API documentation:

1. **Overview** - what the feature does, why it exists
2. **Implementation** - how to implement/use it
3. **Configuration** - how to configure it
4. **API Reference** - detailed method/property descriptions
5. **Examples** - complete working examples
6. **Best Practices** - tips and recommendations
7. **Version History** - when introduced, changes over time
8. **References** - links to related documentation

### Heading Hierarchy

Use semantic heading levels:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```

### Information Boxes

Use blockquotes for special notices:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```

### Lists and Organization

**Unordered lists** for non-sequential items:
```markdown
- First item
- Second item
- Third item
```

**Ordered lists** for sequential steps:
```markdown
1. First step
2. Second step
3. Third step
```

**Definition lists** for term explanations:
```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```

---

## Common Pitfalls to Avoid

### 1. Confusing Similar Systems

**Don't confuse:**
- ClientAppManager registry vs. PortMapper
- i2ptunnel tunnel types vs. port mapper service constants
- ClientApp vs. RouterApp (different contexts)
- Managed vs. unmanaged clients

**Always clarify which system** you're discussing:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```

### 2. Outdated Version References

**Don't:**
- Reference old versions as "current"
- Link to outdated API documentation
- Use deprecated method signatures in examples

**Do:**
- Check release notes before publishing
- Verify API documentation matches current version
- Update examples to use current best practices

### 3. Inaccessible URLs

**Don't:**
- Link only to .i2p domains without clearnet alternatives
- Use broken or outdated documentation URLs
- Link to local file:// paths

**Do:**
- Provide clearnet alternatives for all I2P-internal links
- Verify URLs are accessible before publishing
- Use persistent URLs (geti2p.net, not temporary hosting)

### 4. Incomplete Code Examples

**Don't:**
- Show fragments without context
- Omit error handling
- Use undefined variables
- Skip import statements when not obvious

**Do:**
- Show complete, compilable examples
- Include necessary error handling
- Explain what each significant line does
- Test examples before publishing

### 5. Ambiguous Statements

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```

---

## Markdown Conventions

### File Naming

Use kebab-case for file names:
- `managed-clients.md`
- `port-mapper-guide.md`
- `configuration-reference.md`

### Frontmatter Format

Always include YAML frontmatter:

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```

### Link Formatting

**Internal links** (within documentation):
```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```

**External links** (to other resources):
```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```

**Code repository links**:
```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```

### Table Formatting

Use GitHub-flavored Markdown tables:

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```

### Code Block Language Tags

Always specify language for syntax highlighting:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```

---

## Review Checklist

Before publishing documentation, verify:

- [ ] All technical claims verified against source code or official documentation
- [ ] Version numbers and dates are current
- [ ] All URLs are accessible from clearnet (or alternatives provided)
- [ ] Code examples are complete and tested
- [ ] Terminology follows I2P conventions
- [ ] No em-dashes (use regular dashes or other punctuation)
- [ ] Frontmatter is complete and accurate
- [ ] Heading hierarchy is semantic (h1 → h2 → h3)
- [ ] Lists and tables are properly formatted
- [ ] References section includes all cited sources
- [ ] Document follows the structure guidelines
- [ ] Tone is professional but accessible
- [ ] Similar concepts are clearly distinguished
- [ ] No broken links or references
- [ ] Configuration examples are valid and current


---

**Feedback:** If you find issues or have suggestions for these guidelines, please submit them through the official I2P development channels.
