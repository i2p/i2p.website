---
title: "I2PTunnel"
description: "Tool for interfacing with and providing services on I2P"
slug: "i2ptunnel"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---


## Overview {#overview}

I2PTunnel is a tool for interfacing with and providing services on I2P.
Destination of an I2PTunnel can be defined using a [hostname](/docs/overview/naming),
[Base32](/docs/overview/naming#base32), or a full 516-byte destination key.
An established I2PTunnel will be available on your client machine as localhost:port.
If you wish to provide a service on I2P network, you simply create I2PTunnel to the
appropriate ip_address:port. A corresponding 516-byte destination key will be generated
for the service and it will become available throughout I2P.
A web interface for I2PTunnel management is available on
[localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/).


## Default Services {#default-services}

### Server Tunnels {#default-server-tunnels}

- **I2P Webserver** - A tunnel pointed to a Jetty webserver run
  on [localhost:7658](http://localhost:7658) for convenient and quick hosting on I2P.
  The document root is:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, which expands to: `C:\Users\**username**\AppData\Local\I2P\I2P Site\docroot`


### Client Tunnels {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - A HTTP proxy used for browsing I2P and the regular internet anonymously through I2P. Browsing internet through I2P uses a random proxy specified by the "Outproxies:" option.
- **Irc2P** - *localhost:6668* - An IRC tunnel to the default anonymous IRC network, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - SSH access to the project Git repository
- **smtp.postman.i2p** - *localhost:7659* - A SMTP service provided by postman at hq.postman.i2p
- **pop3.postman.i2p** - *localhost:7660* - The accompanying POP service of postman at hq.postman.i2p


## Configuration {#configuration}

[I2PTunnel Configuration](/docs/specs/configuration)


## Client Modes {#client-modes}

### Standard {#client-modes-standard}

Opens a local TCP port that connects to a service (like HTTP, FTP or SMTP) on a destination inside of I2P.
The tunnel is directed to a random host from the comma separated (", ") list of destinations.


### HTTP {#client-mode-http}

A HTTP-client tunnel. The tunnel connects to the destination specified by the URL
in a HTTP request. Supports proxying onto internet if an outproxy is provided. Strips HTTP connections of the following headers:

- **Accept\*:** (not including "Accept" and "Accept-Encoding") as they vary greatly between browsers and can be used as an identifier.
- **Referer:**
- **Via:**
- **From:**

The HTTP client proxy provides a number of services to protect the user
and to provide a better user experience.

**Request header processing:**
- Strip privacy-problematic headers
- Routing to local or remote outproxy
- Outproxy selection, caching, and reachability tracking
- Hostname to destination lookups
- Host header replacement to b32
- Add header to indicate support for transparent decompression
- Force connection: close
- RFC-compliant proxy support
- RFC-compliant hop-by-hop header processing and stripping
- Optional digest and basic username/password authentication
- Optional outproxy digest and basic username/password authentication
- Buffering of all headers before passing through for efficiency
- Jump server links
- Jump response processing and forms (address helper)
- Blinded b32 processing and credential forms
- Supports standard HTTP and HTTPS (CONNECT) requests

**Response header processing:**
- Check for whether to decompress response
- Force connection: close
- RFC-compliant hop-by-hop header processing and stripping
- Buffering of all headers before passing through for efficiency

**HTTP error responses:**
- For many common and not-so-common errors, so the user knows what happened
- Over 20 unique translated, styled, and formatted error pages for various errors
- Internal web server to serve forms, CSS, images, and errors


#### Transparent Response Compression {#transparent-response-compression}

The i2ptunnel response compression is requested with the HTTP header:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

The server side strips this hop-by-hop header before sending the request to the web server.
The elaborate header with all the q values is not necessary;
servers should just look for "x-i2p-gzip" anywhere in the header.

The server side determines whether to compress the response based on
the headers received from the webserver, including
Content-Type, Content-Length, and Content-Encoding,
to assess if the response is compressible and is worth the additional CPU required.
If the server side compresses the response, it adds the following HTTP header:

- **Content-Encoding:** x-i2p-gzip

If this header is present in the response,
the HTTP client proxy transparently decompresses it.
The client side strips this header and gunzips before sending the response to the browser.
Note that we still have the underlying gzip compression at the I2CP layer,
which is still effective if the response is not compressed at the HTTP layer.

This design and the current implementation violate RFC 2616 in several ways:

- X-Accept-Encoding is not a standard header
- Does not dechunk/chunk per-hop; it passes through chunking end-to-end
- Passes Transfer-Encoding header through end-to-end
- Uses Content-Encoding, not Transfer-Encoding, to specify the per-hop encoding
- Prohibits x-i2p gzipping when Content-Encoding is set (but we probably don't want to do that anyway)
- The server side gzips the server-sent chunking, rather than doing dechunk-gzip-rechunk and dechunk-gunzip-rechunk
- The gzipped content is not chunked afterwards. RFC 2616 requires that all Transfer-Encoding other than "identity" is chunked.
- Because there is no chunking outside (after) the gzip, it is more difficult to find the end of the data, making any implementation of keepalive harder.
- RFC 2616 says Content-Length must not be sent if Transfer-Encoding is present, but we do. The spec says ignore Content-Length if Transfer-Encoding is present, which the browsers do, so it works for us.

Changes to implement a standards-compliant hop-by-hop compression in a backward-compatible
manner are a topic for further study.
Any change to dechunk-gzip-rechunk would require a new encoding type, perhaps
x-i2p-gzchunked.
This would be identical to Transfer-Encoding: gzip, but would have to be
signalled differently for compatibility reasons.
Any change would require a formal proposal.


#### Transparent Request Compression {#transparent-request-compression}

Not supported, although POST would benefit.
Note that we still have the underlying gzip compression at the I2CP layer.


#### Persistence {#persistence}

The client and server proxies do not currently support RFC 2616 HTTP persistent sockets
on any of the three hops (browser socket, I2P socket, server socket).
Connection: close headers are injected at every hop.
Changes to implement persistence are under investigation.
These changes should be standards-compliant and backwards-compatible,
and would not require a formal proposal.


#### Pipelining {#pipelining}

The client and server proxies do not currently support RFC 2616 HTTP pipelining
and there are no plans to do so.
Modern browsers do not support pipelining through proxies because
most proxies cannot implement it correctly.


#### Compatibility {#compatibility}

Proxy implementations must work correctly with other implementations
on the other side. Client proxies should work without a
HTTP-aware server proxy (i.e. a standard tunnel) on the server side.
Not all implementations support x-i2p-gzip.


#### User Agent {#user-agent}

Depending on if the tunnel is using an outproxy or not it will append the following User-Agent:

- *Outproxy:* **User-Agent:** Uses the user agent from a recent Firefox release on Windows
- *Internal I2P use:* **User-Agent:** MYOB/6.66 (AN/ON)


### IRC Client {#client-mode-irc}

Creates a connection to a random IRC server specified by the comma separated (", ")
list of destinations. Only a whitelisted subset of IRC commands are allowed due to anonymity concerns.

The following allow list is for commands inbound from the IRC server to the IRC client.

**Allow list:**
- AUTHENTICATE
- CAP
- ERROR
- H
- JOIN
- KICK
- MODE
- NICK
- PART
- PING
- PROTOCTL
- QUIT
- TOPIC
- WALLOPS

There is also an allow list for commands outbound from the IRC client to the IRC server.
It is quite large due to the number of IRC administrative commands.
See the IRCFilter.java source for details.

The outbound filter also modifies the following commands to strip identifying information:
- NOTICE
- PART
- PING
- PRIVMSG
- QUIT
- USER


### SOCKS 4/4a/5 {#client-mode-socks}

Enables using the I2P router as a SOCKS proxy.


### SOCKS IRC {#client-mode-socks-irc}

Enables using the I2P router as a SOCKS proxy with the command whitelist specified by
[IRC](#client-mode-irc) client mode.


### CONNECT {#client-mode-connect}

Creates a HTTP tunnel and uses the HTTP request method "CONNECT"
to build a TCP tunnel that usually is used for SSL and HTTPS.


### Streamr {#client-mode-streamr}

Creates a UDP-server attached to a Streamr client I2PTunnel. The streamr client tunnel will
subscribe to a streamr server tunnel.

![Streamr diagram](/images/I2PTunnel-streamr.png)


## Server Modes {#server-modes}

### Standard {#server-mode-standard}

Creates a destination to a local ip:port with an open TCP port.


### HTTP {#server-mode-http}

Creates a destination to a local HTTP server ip:port. Supports gzip for requests with
Accept-encoding: x-i2p-gzip, replies with Content-encoding: x-i2p-gzip in such a request.

The HTTP server proxy provides a number of services to make hosting a website easier and more secure,
and to provide a better user experience on the client side.

**Request header processing:**
- Header validation
- Header spoof protection
- Header size checks
- Optional inproxy and user-agent rejection
- Add X-I2P headers so the webserver knows where the request came from
- Host header replacement to make webserver vhosts easier
- Force connection: close
- RFC-compliant hop-by-hop header processing and stripping
- Buffering of all headers before passing through for efficiency

**DDoS protection:**
- POST throttling
- Timeouts and slowloris protection
- Additional throttling happens in streaming for all tunnel types

**Response header processing:**
- Stripping of some privacy-problematic headers
- Mime type and other headers check for whether to compress response
- Force connection: close
- RFC-compliant hop-by-hop header processing and stripping
- Buffering of all headers before passing through for efficiency

**HTTP error responses:**
- For many common and not-so-common errors and on throttling, so the client-side user knows what happened

**Transparent response compression:**
- The web server and/or the I2CP layer may compress, but the web server often does not, and it's most efficient to compress at a high layer, even if I2CP also compresses. The HTTP server proxy works cooperatively with the client-side proxy to transparently compress responses.


### HTTP Bidirectional {#server-mode-http-bidir}

*Deprecated*

Functions as both a I2PTunnel HTTP Server, and a I2PTunnel HTTP client with no outproxying
capabilities. An example application would be a web application that does client-type
requests, or loopback-testing an I2P Site as a diagnostic tool.


### IRC Server {#server-mode-irc}

Creates a destination that filters the registration sequence of a client and passes
the clients destination key as a hostname to the IRC-server.


### Streamr {#server-mode-streamr}

A UDP-client that connects to a media server is created. The UDP-Client is coupled with a Streamr server I2PTunnel.
