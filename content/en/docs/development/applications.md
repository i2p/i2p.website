---
title: "Application Development"
description: "Why write I2P-specific apps, key concepts, development options, and a getting-started guide"
slug: "applications"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## Why Write I2P-Specific Code?

There are multiple ways to use applications in I2P. Using [I2PTunnel](/docs/api/i2ptunnel/), you can use regular applications without needing to program explicit I2P support. This is very effective for client-server scenarios, where you need to connect to a single website. You can simply create a tunnel using I2PTunnel to connect to that website, as shown in Figure 1.

If your application is distributed, it will require connections to a large amount of peers. Using I2PTunnel, you will need to create a new tunnel for each peer you want to contact, as shown in Figure 2. This process can of course be automated, but running a lot of I2PTunnel instances creates a large amount of overhead. In addition, with many protocols you will need to force everyone to use the same set of ports for all peers — e.g. if you want to reliably run DCC chat, everyone needs to agree that port 10001 is Alice, port 10002 is Bob, port 10003 is Charlie, and so on, since the protocol includes TCP/IP specific information (host and port).

General network applications often send a lot of additional data that could be used to identify users. Hostnames, port numbers, time zones, character sets, etc. are often sent without informing the user. As such, designing the network protocol specifically with anonymity in mind can avoid compromising user identities.

There are also efficiency considerations to review when determining how to interact on top of I2P. The streaming library and things built on top of it operate with handshakes similar to TCP, while the core I2P protocols (I2NP and I2CP) are strictly message based (like UDP or in some instances raw IP). The important distinction is that with I2P, communication is operating over a long fat network — each end to end message will have nontrivial latencies, but may contain payloads of up to several KB. An application that needs a simple request and response can get rid of any state and drop the latency incurred by the startup and teardown handshakes by using (best effort) datagrams without having to worry about MTU detection or fragmentation of messages.

![Creating a server-client connection using I2PTunnel only requires creating a single tunnel.](/images/i2ptunnel_serverclient.png)

*Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.*

![Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.](/images/i2ptunnel_peertopeer.png)

*Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.*

In summary, a number of reasons to write I2P-specific code:

- Creating a large amount of I2PTunnel instances consumes a non-trivial amount of resources, which is problematic for distributed applications (a new tunnel is required for each peer).
- General network protocols often send a lot of additional data that can be used to identify users. Programming specifically for I2P allows the creation of a network protocol that does not leak such information, keeping users anonymous and secure.
- Network protocols designed for use on the regular internet can be inefficient on I2P, which is a network with a much higher latency.

I2P supports a standard [plugins interface](/docs/specs/plugin/) for developers so that applications may be easily integrated and distributed.

Applications written in Java and accessible/runnable using an HTML interface via the standard webapps/app.war may be considered for inclusion in the I2P distribution.

---

## Important Concepts

There are a few changes that require adjusting to when using I2P:

### Destination ~= host+port

An application running on I2P sends messages from and receives messages to a unique cryptographically secure end point — a "destination". In TCP or UDP terms, a destination could (largely) be considered the equivalent of a hostname plus port number pair, though there are a few differences.

- An I2P destination itself is a cryptographic construct — all data sent to one is encrypted as if there were universal deployment of IPsec with the (anonymized) location of the end point signed as if there were universal deployment of DNSSEC.
- I2P destinations are mobile identifiers — they can be moved from one I2P router to another (or it can even "multihome" — operate on multiple routers at once). This is quite different from the TCP or UDP world where a single end point (port) must stay on a single host.
- I2P destinations are ugly and large — behind the scenes, they contain a 2048 bit ElGamal public key for encryption, a 1024 bit DSA public key for signing, and a variable size certificate, which may contain proof of work or blinded data.

  There are existing ways to refer to these large and ugly destinations by short and pretty names (e.g. "irc.duck.i2p"), but those techniques do not guarantee globally uniqueness (since they're stored locally in a database on each person's machine) and the current mechanism is not especially scalable nor secure (updates to the host list are managed using "subscriptions" to naming services). There may be some secure, human readable, scalable, and globally unique, naming system some day, but applications shouldn't depend upon it being in place, since there are those who don't think such a beast is possible. [Further information on the naming system](/docs/overview/naming/) is available.

While most applications do not need to distinguish protocols and ports, I2P *does* support them. Complex applications may specify a protocol, from port, and to port, on a per-message basis, to multiplex traffic on a single destination. See the [datagram page](/docs/api/datagrams/) for details. Simple applications operate by listening for "all protocols" on "all ports" of a destination.

### Anonymity and Confidentiality

I2P has transparent end to end encryption and authentication for all data passed over the network — if Bob sends to Alice's destination, only Alice's destination can receive it, and if Bob is using the datagrams or streaming library, Alice knows for certain that Bob's destination is the one who sent the data.

Of course, I2P transparently anonymizes the data sent between Alice and Bob, but it does nothing to anonymize the content of what they send. For instance, if Alice sends Bob a form with her full name, government IDs, and credit card numbers, there is nothing I2P can do. As such, protocols and applications should keep in mind what information they are trying to protect and what information they are willing to expose.

### I2P Datagrams Can Be Up to Several KB

Applications that use I2P datagrams (either raw or repliable ones) can essentially be thought of in terms of UDP — the datagrams are unordered, best effort, and connectionless — but unlike UDP, applications don't need to worry about MTU detection and can simply fire off large datagrams. While the upper limit is nominally 32 KB, the message is fragmented for transport, thus dropping the reliability of the whole. Datagrams over about 10 KB are not currently recommended. See the [datagram page](/docs/api/datagrams/) for details. For many applications, 10 KB of data is sufficient for an entire request or response, allowing them to transparently operate in I2P as a UDP-like application without having to write fragmentation, resends, etc.

---

## Development Options

There are several means of sending data over I2P, each with their own pros and cons. The streaming lib is the recommended interface, used by the majority of I2P applications.

### Streaming Lib

The [full streaming library](/docs/api/streaming/) is now the standard interface. It allows programming using TCP-like sockets, as explained in the [Streaming development guide](#developing-with-the-streaming-library).

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

---

## Start Developing — A Simple Guide

Developing using I2P requires a working I2P installation and a development environment of your own choice. If you are using Java, you can start development with the [streaming library](#developing-with-the-streaming-library) or datagram library. Using another programming language, SAM or BOB can be used.

### Developing with the Streaming Library

The following example shows how to create TCP-like client and server applications using the streaming library.

This will require the following libraries in your classpath:

- `$I2P/lib/streaming.jar`: The streaming library itself
- `$I2P/lib/mstreaming.jar`: Factory and interfaces for the streaming library
- `$I2P/lib/i2p.jar`: Standard I2P classes, data structures, API, and utilities

You can fetch these from an I2P installation, or add the following dependencies from Maven Central:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

Network communication requires the usage of I2P network sockets. To demonstrate this, we will create an application where a client can send text messages to a server, who will print the messages and send them back to the client. In other words, the server will function as an echo.

We will start by initializing the server application. This requires getting an I2PSocketManager and creating an I2PServerSocket. We will not provide the I2PSocketManagerFactory with the saved keys for an existing Destination, so it will create a new Destination for us. So we will ask the I2PSocketManager for an I2PSession, so we can find out the Destination that was created, as we will need to copy and paste that information later so the client can connect to us.

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```

*Code example 1: initializing the server application.*

Once we have an I2PServerSocket, we can create I2PSocket instances to accept connections from clients. In this example, we will create a single I2PSocket instance, that can only handle one client at a time. A real server would have to be able to handle multiple clients. To do this, multiple I2PSocket instances would have to be created, each in separate threads. Once we have created the I2PSocket instance, we read data, print it and send it back to the client.

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```

*Code example 2: accepting connections from clients and handling messages.*

When you run the above server code, it should print something like this (but without the line endings, it should just be one huge block of characters):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```

This is the base64-representation of the server Destination. The client will need this string to reach the server.

Now, we will create the client application. Again, a number of steps are required for initialization. Again, we will need to start by getting an I2PSocketManager. We won't use an I2PSession and an I2PServerSocket this time. Instead, we will use the server Destination string to start our connection. We will ask the user for the Destination string, and create an I2PSocket using this string. Once we have an I2PSocket, we can start sending and receiving data to and from the server.

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```

*Code example 3: starting the client and connecting it to the server application.*

Finally, you can run both the server and the client application. First, start the server application. It will print a Destination string (like shown above). Next, start the client application. When it requests a Destination string, you can enter the string printed by the server. The client will then send 'Hello I2P!' (along with a newline) to the server, who will print the message and send it back to the client.

Congratulations, you have successfully communicated over I2P!

---

## Existing Applications

Contact us if you would like to contribute.

- [I2P-Bote](http://i2pbote.i2p/) - contact HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

See also all the plugins on [plugins.i2p](http://plugins.i2p/), the applications and source code listed on [echelon.i2p](http://echelon.i2p/), and the application code hosted on [git.repo.i2p](http://git.repo.i2p/).

See also the bundled applications in the I2P distribution - SusiMail and I2PSnark.

---

## Application Ideas

- NNTP server - there have been some in the past, none at the moment
- Jabber server - there have been some in the past, and there is one at the moment, with access to the public internet
- PGP Key server and/or proxy
- Content Distribution / DHT applications - resurrect feedspace, port dijjer, look for alternatives
- Help out with [Syndie](http://syndie.i2p2.de/) development
- Web-based applications - The sky is the limit for hosting web-server-based applications such as blogs, pastebins, storage, tracking, feeds, etc. Any web or CGI technology such as Perl, PHP, Python, or Ruby will work.
- Resurrect some old apps, several previously in the i2p source package - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
