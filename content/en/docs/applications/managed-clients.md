---
title: "Managed Clients"
description: "How router-managed applications integrate with ClientAppManager and the port mapper"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---


## 1. Overview

Entries in [`clients.config`](/docs/specs/configuration/#clients-config) tell the router which applications to launch on startup. Each entry may run as a **managed** client (preferred) or as an **unmanaged** client. Managed clients collaborate with `ClientAppManager`, which:

- Instantiates the application and tracks lifecycle state for the router console
- Exposes start/stop controls to the user and enforces clean shutdowns at router exit
- Hosts a lightweight **client registry** and **port mapper** so applications can discover each other's services

Unmanaged clients simply invoke a `main()` method; use them only for legacy code that cannot be modernized.

## 2. Implementing a Managed Client

Managed clients must implement either `net.i2p.app.ClientApp` (for user-facing apps) or `net.i2p.router.app.RouterApp` (for router extensions). Provide one of the constructors below so the manager can supply context and configuration arguments:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```

```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```

The `args` array contains the values configured in `clients.config` or individual files in `clients.config.d/`. Extend `ClientApp` / `RouterApp` helper classes when possible to inherit default lifecycle wiring.

### 2.1 Lifecycle Methods

Managed clients are expected to implement:

- `startup()` - perform initialization and return promptly. Must call `manager.notify()` at least once to transition from INITIALIZED state.
- `shutdown(String[] args)` - release resources and stop background threads. Must call `manager.notify()` at least once to change state to STOPPING or STOPPED.
- `getState()` - inform the console whether the app is running, starting, stopping, or failed

The manager calls these methods as users interact with the console.

### 2.2 Advantages

- Accurate status reporting in the router console
- Clean restarts without leaking threads or static references
- Lower memory footprint once the application stops
- Centralized logging and error reporting via the injected context

## 3. Unmanaged Clients (Fallback Mode)

If the configured class does not implement a managed interface, the router launches it by invoking `main(String[] args)` and cannot track the resulting process. The console shows limited information and shutdown hooks may not run. Reserve this mode for scripts or one-off utilities that cannot adopt the managed APIs.

## 4. Client Registry

Managed and unmanaged clients may register themselves with the manager so other components can retrieve a reference by name:

```java
manager.register(this);
```

The registration uses the client's `getName()` return value as the registry key. Known registrations include `console`, `i2ptunnel`, `Jetty`, `outproxy`, and `update`. Retrieve a client with `ClientAppManager.getRegisteredApp(String name)` to coordinate features (for example, the console querying Jetty for status details).

Note that client registry and port mapper are separate systems. The client registry enables inter-application communication by name lookup, while the port mapper maps service names to host:port combinations for service discovery.

## 5. Port Mapper

The port mapper offers a simple directory for internal TCP services. Register loopback ports so collaborators avoid hardcoded addresses:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```

Or with explicit host specification:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```

Look up services using `PortMapper.getPort(String name)` (returns -1 if not found) or `getPort(String name, int defaultPort)` (returns default if not found). Check registration status with `isRegistered(String name)` and retrieve the registered host with `getActualHost(String name)`.

Common port mapper service constants from `net.i2p.util.PortMapper`:

- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_HTTPS_PROXY` - HTTPS proxy (default port 4445)
- `SVC_I2PTUNNEL` - I2PTunnel manager
- `SVC_SAM` - SAM bridge (default port 7656)
- `SVC_SAM_SSL` - SAM bridge SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - BOB bridge (default port 2827)
- `SVC_EEPSITE` - Standard eepsite (default port 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS eepsite
- `SVC_IRC` - IRC tunnel (default port 6668)
- `SVC_SUSIDNS` - SusiDNS

Note: `httpclient`, `httpsclient`, and `httpbidirclient` are i2ptunnel tunnel types (used in `tunnel.N.type` configuration), not port mapper service constants.

## 6. Configuration Format

### 6.1 Modern Structure (0.9.42 and later)

As of version 0.9.42, the router supports splitting configuration into individual files within `clients.config.d/` directory. Each file contains properties for a single client with all properties prefixed `clientApp.0.`:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```

This is the recommended approach for new installations and plugins.

### 6.2 Legacy Format (monolithic clients.config)

For backward compatibility, the traditional format uses sequential numbering:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```

### 6.3 Configuration Properties

**Required:**
- `main` - Full class name implementing ClientApp or RouterApp, or containing static `main(String[] args)`

**Optional:**
- `name` - Display name for router console (defaults to class name)
- `args` - Space or tab-separated arguments (supports quoted strings)
- `delay` - Seconds before starting (default 120)
- `onBoot` - Forces `delay=0` if true
- `startOnLoad` - Enables/disables the client (default true)

**Plugin-specific:**
- `stopargs` - Arguments passed during shutdown
- `uninstallargs` - Arguments passed during plugin uninstall
- `classpath` - Comma-separated additional classpath entries

**Variable substitution for plugins:**
- `$I2P` - I2P base directory
- `$CONFIG` - User configuration directory (e.g., ~/.i2p)
- `$PLUGIN` - Plugin directory
- `$OS` - Operating system name
- `$ARCH` - Architecture name

## 7. Best Practices

- Prefer managed clients; fall back to unmanaged only when absolutely necessary.
- Keep initialization and shutdown lightweight so console operations remain responsive.
- Use descriptive registry and port names so diagnostic tools (and end users) understand what a service does.
- Avoid static singletons - rely on the injected context and manager to share resources.
- Call `manager.notify()` on all state transitions to maintain accurate console status.
- If you must run in a separate JVM, document how logs and diagnostics are surfaced to the main console.
- For external programs, consider using ShellService (added in version 1.7.0) to gain managed client benefits.

## 8. API Stability and Version History

Managed clients were introduced in **version 0.9.4** (December 17, 2012) and remain the recommended architecture as of **version 2.10.0** (September 9, 2025). The core APIs have remained stable with zero breaking changes across this period:

- Constructor signatures unchanged
- Lifecycle methods (startup, shutdown, getState) unchanged
- ClientAppManager registration methods unchanged
- PortMapper registration and lookup methods unchanged

Notable enhancements:
- **0.9.42 (2019)** - clients.config.d/ directory structure for individual configuration files
- **1.7.0 (2021)** - ShellService added for external program state tracking
- **2.10.0 (2025)** - Current release with no managed client API changes

The next major release will require Java 17+ as a minimum (infrastructure requirement, not an API change).

## References

- [clients.config specification](/docs/specs/configuration/#clients-config)
- [Configuration File Specification](/docs/specs/configuration/)
- [I2P Technical Documentation Index](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [ClientApp interface](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [RouterApp interface](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Alternative Javadoc (stable)](https://docs.i2p-projekt.de/javadoc/)
- [Alternative Javadoc (clearnet mirror)](https://eyedeekay.github.io/javadoc-i2p/)

> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ which requires an I2P router for access. For clearnet access, use the GitHub Pages mirror above.
