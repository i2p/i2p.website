---
title: "Managed Clients"
description: "How router-managed applications integrate with ClientAppManager and the port mapper"
slug: "managed-clients"
lastUpdated: "2014-02"
accurateFor: "0.9.11"
---

## Overview

Clients may be started directly by the router when they are listed in the [clients.config](/docs/specs/configuration/) file. These clients may be "managed" or "unmanaged". This is handled by the ClientAppManager. Additionally, managed or unmanaged clients may register with the ClientAppManager so that other clients may retrieve a reference to them. There is also a simple Port Mapper facility for clients to register an internal port that other clients may look up.

---

## Managed Clients

As of release 0.9.4, the router supports managed clients. Managed clients are instantiated and started by the ClientAppManager. The ClientAppManager maintains a reference to the client and receives updates on the client's state. Managed clients are preferred, as it is much easier to implement state tracking and to start and stop a client. It also is much easier to avoid static references in the client code which could lead to excessive memory usage after a client is stopped. Managed clients may be started and stopped by the user in the router console, and are stopped at router shutdown.

Managed clients implement either the net.i2p.app.ClientApp or net.i2p.router.app.RouterApp interface. Clients implementing the ClientApp interface must provide the following constructor:

```java
public MyClientApp(I2PAppContext context, ClientAppManager listener, String[] args)
```

Clients implementing the RouterApp interface must provide the following constructor:

```java
public MyClientApp(RouterContext context, ClientAppManager listener, String[] args)
```

The arguments provided are specified in the clients.config file.

---

## Unmanaged Clients

If the main class specified in the clients.config file does not implement a managed interface, it will be started with main() with the arguments specified, and stopped with main() with the arguments specified. The router does not maintain a reference, since all interactions are via the static main() method. The console cannot provide accurate state information to the user.

---

## Registered Clients

Clients, whether managed or unmanaged, may register with the ClientAppManager so that other clients may retrieve a reference to them. Registration is by name. Known registered clients are:

```
console, i2ptunnel, Jetty, outproxy, update
```

---

## Port Mapper

The router also provides a simple mechanism for clients to find an internal socket service, such as the HTTP proxy. This is provided by the Port Mapper. Registration is by name. Clients that register generally provide an internal emulated socket on that port.
