---
title: "Application Development"
description: "Why write I2P-specific apps, key concepts, development options, and a simple getting-started guide"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Why Write I2P-Specific Code?

There are multiple ways to use applications in I2P. Using [I2PTunnel](/docs/api/i2ptunnel/), you can use regular applications without needing to program explicit I2P support. This is very effective for client-server scenarios, where you need to connect to a single website. You can simply create a tunnel using I2PTunnel to connect to that website, as shown in Figure 1.

If your application is distributed, it will require connections to a large amount of peers. Using I2PTunnel, you will need to create a new tunnel for each peer you want to contact, as shown in Figure 2. This process can of course be automated, but running a lot of I2PTunnel instances creates a large amount of overhead. In addition, with many protocols you will need to force everyone to use the same set of ports for all peers — e.g. if you want to reliably run DCC chat, everyone needs to agree that port 10001 is Alice, port 10002 is Bob, port 10003 is Charlie, and so on, since the protocol includes TCP/IP specific information (host and port).

General network applications often send a lot of additional data that could be used to identify users. Hostnames, port numbers, time zones, character sets, etc. are often sent without informing the user. As such, designing the network protocol specifically with anonymity in mind can avoid compromising user identities.

There are also efficiency considerations to review when determining how to interact on top of I2P. The streaming library and things built on top of it operate with handshakes similar to TCP, while the core I2P protocols (I2NP and I2CP) are strictly message based (like UDP or in some instances raw IP). The important distinction is that with I2P, communication is operating over a long fat network — each end to end message will have nontrivial latencies, but may contain payloads of up to several KB. An application that needs a simple request and response can get rid of any state and drop the latency incurred by the startup and teardown handshakes by using (best effort) datagrams without having to worry about MTU detection or fragmentation of messages.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>

In summary, a number of reasons to write I2P-specific code:

- Creating a large amount of I2PTunnel instances consumes a non-trivial amount of resources, which is problematic for distributed applications (a new tunnel is required for each peer).
- General network protocols often send a lot of additional data that can be used to identify users. Programming specifically for I2P allows the creation of a network protocol that does not leak such information, keeping users anonymous and secure.
- Network protocols designed for use on the regular internet can be inefficient on I2P, which is a network with a much higher latency.

I2P supports a standard [plugins interface](/docs/specs/plugin/) for developers so that applications may be easily integrated and distributed.

Applications written in Java and accessible/runnable using an HTML interface via the standard webapps/app.war may be considered for inclusion in the I2P distribution.

## Important Concepts

There are a few changes that require adjusting to when using I2P:

### Destinations

An application running on I2P sends messages from and receives messages to a unique cryptographically secure end point — a "destination". In TCP or UDP terms, a destination could (largely) be considered the equivalent of a hostname plus port number pair, though there are a few differences.

- An I2P destination itself is a cryptographic construct — all data sent to one is encrypted as if there were universal deployment of IPsec with the (anonymized) location of the end point signed as if there were universal deployment of DNSSEC.
- I2P destinations are mobile identifiers — they can be moved from one I2P router to another (or it can even "multihome" — operate on multiple routers at once). This is quite different from the TCP or UDP world where a single end point (port) must stay on a single host.
- I2P destinations are ugly and large — behind the scenes, they contain a 2048 bit ElGamal public key for encryption, a 1024 bit DSA public key for signing, and a variable size certificate, which may contain proof of work or blinded data.

  There are existing ways to refer to these large and ugly destinations by short and pretty names (e.g. "irc.duck.i2p"), but those techniques do not guarantee globally uniqueness (since they're stored locally in a database on each person's machine) and the current mechanism is not especially scalable nor secure (updates to the host list are managed using "subscriptions" to naming services). There may be some secure, human readable, scalable, and globally unique, naming system some day, but applications shouldn't depend upon it being in place. [Further information on the naming system](/docs/overview/naming/) is available.

While most applications do not need to distinguish protocols and ports, I2P *does* support them. Complex applications may specify a protocol, from port, and to port, on a per-message basis, to multiplex traffic on a single destination. See the [datagram page](/docs/api/datagrams/) for details. Simple applications operate by listening for "all protocols" on "all ports" of a destination.

### Anonymity and Confidentiality

I2P has transparent end to end encryption and authentication for all data passed over the network — if Bob sends to Alice's destination, only Alice's destination can receive it, and if Bob is using the datagrams or streaming library, Alice knows for certain that Bob's destination is the one who sent the data.

Of course, I2P transparently anonymizes the data sent between Alice and Bob, but it does nothing to anonymize the content of what they send. For instance, if Alice sends Bob a form with her full name, government IDs, and credit card numbers, there is nothing I2P can do. As such, protocols and applications should keep in mind what information they are trying to protect and what information they are willing to expose.

### I2P Datagrams Can Be Up to Several KB

Applications that use I2P datagrams (either raw or repliable ones) can essentially be thought of in terms of UDP — the datagrams are unordered, best effort, and connectionless — but unlike UDP, applications don't need to worry about MTU detection and can simply fire off large datagrams. While the upper limit is nominally 32 KB, the message is fragmented for transport, thus dropping the reliability of the whole. Datagrams over about 10 KB are not currently recommended. See the [datagram page](/docs/api/datagrams/) for details. For many applications, 10 KB of data is sufficient for an entire request or response, allowing them to transparently operate in I2P as a UDP-like application without having to write fragmentation, resends, etc.

## Development Options

There are several means of sending data over I2P, each with their own pros and cons. The streaming lib is the recommended interface, used by the majority of I2P applications.

### Streaming Lib

The [full streaming library](/docs/specs/streaming/) is now the standard interface. It allows programming using TCP-like sockets, as explained in the [Streaming development guide](#developing-with-the-streaming-library).

### BOB

BOB is the [Basic Open Bridge](/docs/legacy/bob/), allowing an application in any language to make streaming connections to and from I2P. At this point in time it lacks UDP support, but UDP support is planned in the near future. BOB also contains several tools, such as destination key generation, and verification that an address conforms to I2P specifications. Up to date info and applications that use BOB can be found at this [I2P Site](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM is not recommended. SAM V2 is okay, SAM V3 is recommended.*

SAM is the [Simple Anonymous Messaging](/docs/legacy/sam/) protocol, allowing an application written in any language to talk to a SAM bridge through a plain TCP socket and have that bridge multiplex all of its I2P traffic, transparently coordinating the encryption/decryption and event based handling. SAM supports three styles of operation:

- streams, for when Alice and Bob want to send data to each other reliably and in order
- repliable datagrams, for when Alice wants to send Bob a message that Bob can reply to
- raw datagrams, for when Alice wants to squeeze the most bandwidth and performance as possible, and Bob doesn't care whether the data's sender is authenticated or not (e.g. the data transferred is self authenticating)

SAM V3 aims at the same goal as SAM and SAM V2, but does not require multiplexing/demultiplexing. Each I2P stream is handled by its own socket between the application and the SAM bridge. Besides, datagrams can be sent and received by the application through datagram communications with the SAM bridge.

[SAM V2](/docs/legacy/samv2/) is a new version used by imule that fixes some of the problems in [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) is used by imule since version 1.4.0.

### I2PTunnel

The I2PTunnel application allows applications to build specific TCP-like tunnels to peers by creating either I2PTunnel 'client' applications (which listen on a specific port and connect to a specific I2P destination whenever a socket to that port is opened) or I2PTunnel 'server' applications (which listen to a specific I2P destination and whenever it gets a new I2P connection it outproxies to a specific TCP host/port). These streams are 8-bit clean, and are authenticated and secured through the same streaming library that SAM uses, but there is a nontrivial overhead involved with creating multiple unique I2PTunnel instances, since each have their own unique I2P destination and their own set of tunnels, keys, etc.

### SOCKS

I2P supports a SOCKS V4 and V5 proxy. Outbound connections work well. Inbound (server) and UDP functionality may be incomplete and untested.

### Ministreaming

*Removed*

There used to be a simple "ministreaming" library, but now ministreaming.jar contains only the interfaces for the full streaming library.

### Datagrams

*Recommended for UDP-like applications*

The [Datagram library](/docs/api/datagrams/) allows sending UDP-like packets. It's possible to use:

- Repliable datagrams
- Raw datagrams

### I2CP

*Not recommended*

[I2CP](/docs/specs/i2cp/) itself is a language independent protocol, but to implement an I2CP library in something other than Java there is a significant amount of code to be written (encryption routines, object marshalling, asynchronous message handling, etc). While someone could write an I2CP library in C or something else, it would most likely be more useful to use the C SAM library instead.

### Web Applications

I2P comes with the Jetty webserver, and configuring to use the Apache server instead is straightforward. Any standard web app technology should work.

## Start Developing — A Simple Guide

Developing using I2P requires a working I2P installation and a development environment of your own choice. If you are using Java, you can start development with the [streaming library](#developing-with-the-streaming-library) or datagram library. Using another programming language, SAM or BOB can be used.

### Developing with the Streaming Library

Below is a trimmed and modernized version of the example in the original page. For the full example, see the legacy page or our Java examples in the codebase.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```

*Code example: basic server receiving data.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```

*Code example: client connecting and sending a line.*
