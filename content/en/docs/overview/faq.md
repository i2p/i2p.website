---
title: "Frequently Asked Questions"
description: "Comprehensive I2P FAQ: router help, configuration, reseeds, privacy/safety, performance, and troubleshooting"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - "/en/faq"
  - "/faq"
  - "/en/faq/"
  - "/faq/"
type: docs
---

<ol>
<li style="list-style: none; display: inline">
<h4></h4>
</li>
<li><a href="#systems">What systems will I2P run on?</a></li>
<li><a href="#java">Is installing Java required to use I2P?</a></li>
<li><a href="#I2P Site">What is an "I2P Site" and how do I configure my browser so I can use them?</a></li>
<li><a href="#active">What do the Active x/y numbers mean in the router console?</a></li>
<li><a href="#peers">My router has very few active peers, is this OK?</a></li>
<li><a href="#badcontent">I am opposed to certain types of content. How do I keep from distributing, storing, or accessing them?</a></li>
<li><a href="#blocking">Is it possible to block I2P?</a></li>
<li><a href="#protocolfamily">In <code>wrapper.log</code> I see an error stating <code>Protocol family unavailable</code> when I2P is loading</a></li>
<li><a href="#down">Most of the I2P Sites within I2P are down?</a></li>
<li><a href="#port32000">Why is I2P listening for connections on port 32000?</a></li>
<li style="list-style: none; display: inline">
<h4></h4>
</li>
<li><a href="#browserproxy">How do I configure my browser?</a></li>
<li><a href="#irc">How do I connect to IRC within I2P?</a></li>
<li><a href="#myI2P Site">How do I set up my own I2P Site?</a></li>
<li><a href="#hosting">If I host a website at I2P at home, containing only HTML and CSS, is it dangerous?</a></li>
<li><a href="#addresses">How Does I2P find ".i2p" websites?</a></li>
<li><a href="#addressbook">How do I add to the Address Book?</a></li>
<li><a href="#ports">What ports does I2P use?</a></li>
<li><a href="#subscriptions">I'm missing lots of hosts in my address book. What are some good subscription links?</a></li>
<li><a href="#remote_webconsole">How can I access the web console from my other machines or password protect it?</a></li>
<li><a href="#remote_i2cp">How can I use applications from my other machines?</a></li>
<li><a href="#socks">Is it possible to use I2P as a SOCKS proxy?</a></li>
<li><a href="#proxy_other">How do I access IRC, BitTorrent, or other services on the regular Internet?</a></li>
<li style="list-style: none; display: inline">
<h4></h4>
</li>
<li><a href="#reseed">My router has been up for several minutes and has zero or very few connections</a></li>
<li><a href="#manual_reseed">How do I reseed manually?</a></li>
<li style="list-style: none; display: inline">
<h4></h4>
</li>
<li><a href="#exit">Is my router an "exit node"(outproxy) to the regular Internet? I don't want it to be.</a></li>
<li><a href="#detection">Is it easy to detect the use of I2P by analyzing network traffic?</a></li>
<li><a href="#safe">Is using I2P Safe?</a></li>
<li><a href="#netdb_ip">I see IP addresses of all other I2P nodes in the router console. Does that mean my IP address is visible by others?</a></li>
<li><a href="#proxy_safe">Is using an outproxy safe?</a></li>
<li><a href="#deanon">What about "De-Anonymizing" attacks?</a></li>
<li style="list-style: none; display: inline">
<h4>Internet Access/Performance</h4>
</li>
<li><a href="#outproxy">I can't access regular Internet sites through I2P.</a></li>
<li><a href="#https">I can't access https:// or ftp:// sites through I2P.</a></li>
<li><a href="#cpu">Why is my router using too much CPU?</a></li>
<li><a href="#peers">My router has very few active peers, is this OK?</a></li>
<li><a href="#vary">My active peers / known peers / participating tunnels / connections / bandwidth vary dramatically over time! Is anything wrong?</a></li>
<li><a href="#slow">What makes downloads, torrents, web browsing, and everything else slower on I2P as compared to the regular internet?</a></li>
<li style="list-style: none; display: inline">
<h4>Bugs and Questions</h4>
</li>
<li><a href="#bug">I think I found a bug, where can I report it?</a></li>
<li><a href="#question">I have a question!</a></li>
</ol>

<h2>I2P Router Help</h2>
<h3 id="systems"><span class="permalink"><a href="#systems">
What systems will I2P run on?</a> </span></h3>
<p>

I2P is written in the <a href="">Java programming language</a>. 
It has been tested on Windows, Linux, FreeBSD and OSX. 
An <a href="">Android port</a> is also available.</p>

<p>In terms of memory usage, I2P is configured to use 128 MB of RAM by default. 
This is sufficient for browsing and IRC usage. However, other activities may require greater memory allocation. 
For example, if one wishes to run a high-bandwidth router, participate in I2P torrents or serve high-traffic hidden services, 
a higher amount of memory is required.</p>

<p>
In terms of CPU usage, I2P has been tested to run on modest systems such as the <a href="">Raspberry Pi</a> range of single-board computers.
As I2P makes heavy use of cryptographic techniques, a stronger CPU will be better suited to handle the workload generated by I2P as well as tasks 
related to the rest of the system (i.e. Operating System, GUI, Other processes e.g. Web Browsing).</p>

<p>A comparison of some of the available Java Runtime Environments (JRE) is available here: 
<a href=""></a>.

Using Sun/Oracle Java or OpenJDK is recommended.
</p>

<h3 id="java"><span class="permalink"><a href="#java">
Is installing Java required to use I2P?</a></span>
</h3>
<p>
Yes, Java is required to use I2P Core. We include Java inside our easy-installers for
Windows, Mac OSX, and Linux. If you’re running the I2P Android app you will also need a
Java runtime like Dalvik or ART installed in most cases.
</p>

<h3 id="I2P Site"><span class="permalink"><a href="#I2P Site">
What is an "I2P Site" and how do I configure my browser so I can use them?</a></span>
</h3>
<p>
An I2P Site is a normal website except that it is hosted inside I2P. I2P sites have
addresses that look like normal internet addresses, ending in ".i2p" in a human-
readable, non-cryptographic way, for the benefit of people. Actually connecting to an
I2P Site requires cryptography, which means that I2P Site addresses are also the long
“Base64” Destinations and the shorter “B32” addresses. You may need to do additional
configuration to browse correctly. Browsing I2P Sites will require activating the HTTP
Proxy in your I2P installation and then configuring your browser to use it. For more
information, browse the “Browsers” section below or the “Browser Configuration” Guide.
</p>

<h3 id="active"><span class="permalink"><a href="#active">
What do the Active x/y numbers mean in the router console?</a></span>
</h3>
<p>
In the Peers page on your router console, you may see two numbers - Active x/y. The 
first number is the number of peers that you’ve sent or received a message to or from in
the last few minutes. The second number is the number of peers seen recently, this will
always be larger than or equal to the first number.
</p>

<h3 id="peers"><span class="permalink"><a href="#peers">
My router has very few active peers, is this OK?</a></span>
</h3>
<p>Yes, this can be normal, especially when the router has just been started. New routers
will need time to startup and connect to the rest of the network. To help improve
network integration, uptime, and performance, review these settings:</p>
<ul>
  <li>
<b>Share bandwidth</b><br> 
If a router is configured to share bandwidth, it will route more traffic for other
routers which helps integrate it with the rest of the network, as well as improving the
performance of one’s local connection. This can be configured on the <a href="http://localhost:7657/config">http://localhost:7657/config</a> page.</li>
  <li>
<b>Network interface</b><br> 
Make sure there is not an interface specified on the <a href="http://localhost:7657/confignet">http://localhost:7657/confignet</a> page. This
can reduce performance unless your computer is multi-homed with multiple external IP
addresses.</li>
  <li>
<b>I2NP protocol</b><br>
Make sure the router is configured to expect connections on a valid protocol for the
host’s operating system and empty network(Advanced) settings. Do not enter an IP address
in the ‘Hostname’ field in the Network configuration page. The I2NP Protocol you select
here will only be used if you do not already have a reachable address. Most Verizon 4G
and 5G wireless connections in the United States, for example, block UDP and can’t be
reached over it. Others would use UDP by force even if it is available to them. Choose a
reasonable setting from the listed I2NP Protocols.
</li>
</ul>

<h3 id="badcontent"><span class="permalink"><a href="#badcontent">
I am opposed to certain types of content. How do I keep from distributing, storing, or accessing them?</a></span>
</h3>
<p>
There is none of this material installed by default. However, since I2P is a peer-to-
peer network, it’s possible that you may encounter prohibited content by accident. Here is a
summary of how I2P prevents you from being unnecessarily involved in violations of your
beliefs.
</p>
<ul>
  <li>
<b>Distribution</b><br>
Traffic is internal to the I2P network, you are not an <a href="#exit">exit node</a> (referred to as an outproxy in our documentation).
</li>
  <li>
<b>Storage</b><br> 
The I2P network does not do distributed storage of content, this has to be specifically installed and configured by the user (with Tahoe-LAFS, for example). 
That is a feature of a different anonymous network, <a href="http://freenetproject.org/">Freenet</a>.
By running an I2P router, you are not storing content for anyone.
</li>
  <li>
<b>Access</b><br>
Your router will not request any content without your specific instruction to do so.</li>
</ul>

<h3 id="blocking"><span class="permalink"><a href="#blocking">Is it possible to block I2P?</a></span></h3>
<p>Yes, by far the easiest and most common way is by blocking bootstrap, or "Reseed" servers. Completely blocking all obfuscated traffic
would work as well (although it would break many, many other things that are not I2P and most are not willing to go this far).
In the case of reseed blocking, there is a reseed bundle on Github, blocking it will also block Github.
You can reseed over a proxy (many can be found on Internet if you do not want to use Tor) or share reseed bundles on a friend-to-friend basis offline.</p>

<h3 id="protocolfamily"><span class="permalink"><a href="#protocolfamily">
In <code>wrapper.log</code> I see an error that states "<code>Protocol family unavailable</code>" when loading the Router Console</a></span>
</h3>
<p>
Often this error will occur with any network enabled java software on some systems that are configured to use IPv6 by default. There are a few ways to solve this:
</p>
<ul>
  <li>
On Linux based systems, you can <code>echo 0 > /proc/sys/net/ipv6/bindv6only</code>
</li>
  <li>Look for the following lines in <code>wrapper.config</code>.<br />
<code>#wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true<br />
      #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false<br />
</code><br />
  If the lines are there, uncomment them by removing the "#"s. If the lines are not there, add them without the "#"s.
  </li>
</ul>
Another option would be to remove the <strong>::1</strong> from <code>~/.i2p/clients.config</code>

<p>
<strong>WARNING</strong>: For any changes to <code>wrapper.config</code> to take effect, you must completely
stop the router and the wrapper. Clicking <em>Restart</em> on your
router console will NOT reread this file! You must
click <em>Shutdown</em>, wait 11 minutes, then start I2P.
</p>

<h3 id="down"><span class="permalink"><a href="#down">
Most of the I2P Sites within I2P are down?</a></span>
</h3>
<p>
If you consider every I2P Site that has ever been created, yes, most of them are down.
People and I2P Sites come and go.
A good way to get started in I2P is check out a list of I2P Sites that are currently up.
<a href="http://identiguy.i2p">identiguy.i2p</a> tracks active I2P Sites.
</p>

<h3 id="port32000"><span class="permalink"><a href="#port32000">
Why is I2P listening on port 32000?</a></span>
</h3>
<p>
The Tanuki java service wrapper that we use opens this port &mdash;bound to localhost&mdash; in order to communicate with software running inside the JVM. 
When the JVM is launched it is given a key so it can connect to the wrapper. 
After the JVM establishes its connection to the wrapper, the wrapper refuses any additional connections.
</p>
<p>
More information can be found in the <a href="http://wrapper.tanukisoftware.com/doc/english/prop-port.html">wrapper documentation</a>.

<h3 id="browserproxy"><span class="permalink"><a href="#browserproxy">
How do I configure my browser?</a></span>
</h3>
<p>
The proxy config for different browsers is on a <a href=""> separate page</a> with screenshots. 
More advanced configs with external tools, such as the browser plug-in FoxyProxy or the proxy server Privoxy, are possible but could introduce leaks in your setup.
</p>

<h3 id="irc"><span class="permalink"><a href="#irc">
How do I connect to IRC within I2P?</a></span>
</h3>
<p>
A tunnel to the main IRC server within I2P, Irc2P, is created when I2P is installed (see the <a href="http://localhost:7657/i2ptunnel/index.jsp">I2PTunnel configuration page</a>), and is automatically started when the I2P router starts. 
To connect to it, tell your IRC client to connect to <code>localhost 6668</code>. 
HexChat-like client users can create a new network with the server <code>localhost/6668</code> (remember to tick "Bypass proxy server" if you have a proxy server configured).
Weechat users can use the following command to add a new network:
</p>
<code>
  <pre>
    /server add irc2p localhost/6668
  </pre>
</code>

<h3 id="myI2P Site"><span class="permalink"><a href="#myI2P Site">
How do I set up my own I2P Site?</a></span>
</h3>
<p>
The easiest method is to click on the <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> link in the router console and create a new 'Server Tunnel'. 
You can serve dynamic content by setting the tunnel destination to the port of an existing webserver, such as Tomcat or Jetty.
You can also serve static content. For this, set the tunnel destination to: <code>0.0.0.0 port 7659</code> and place the content in the <code>~/.i2p/eepsite/docroot/</code> directory. (On non-Linux systems, this may be in a different place. 
Check the router console.) 
The 'eepsite' software comes as part of the I2P installation package and is set to automatically start when I2P is started. 
The default site this creates can be accessed at http://127.0.0.1:7658. 
However, your 'eepsite' is also accessible to others via your eepsite key file, located at: 
<code>~/.i2p/eepsite/i2p/eepsite.keys</code>. To find out more, read the readme file at: <code>~/.i2p/eepsite/README.txt</code>.
</p>

<h3 id="hosting"><span class="permalink"><a href="#hosting">
If I host a website at I2P at home, containing only HTML and CSS, is it dangerous?</a></span>
</h3>
<p>
It depends on your adversary and your threat model. If you are only worried about corporate “privacy” violations, typical criminals and censorship, then it is not really dangerous. 
Law-enforcement will probably find you anyway if they really want to. 
Only hosting when you have a normal (internet) home user browser running will make it really tough to know who is hosting that part. 
Please consider the hosting of your I2P site just as hosting any other service - it is as dangerous - or safe - as you configure and manage it yourself.
<br>
Note: There is already a way to separate hosting an i2p service(destination) from the i2p router. If you <a href="/docs/overview/tech-intro#i2pservices"> understand how</a> it works, then you can just setup a separate machine as a server for the website (or service) that will be publicly accessible and forward that to the webserver over a [very] secure SSH tunnel or use a secured, shared, filesystem.
</p>

<h3 id="addresses">How Does I2P find ".i2p" websites? </h3>
<p>The I2P Address Book application maps human-readable names to long-term destinations, associated with services, making it more like a hosts file or a contact list than a network database or a DNS service. It's also local-first there is no recognized global namespace, you decide what any given .i2p domain maps to in the end. The middle-ground is something called a "Jump Service" which provides a human-readable name by redirecting you to a page where you will be asked "Do you give the I2P router permission to call $SITE_CRYPTO_KEY the name $SITE_NAME.i2p" or something to that effect. Once it's in your address book, you can generate your own jump URL's to help share the site with others. </p>

<h3 id="addressbook">How do I add addresses to the Address Book? </h3>
<p>You cannot add an address without knowing at least the base32 or base64 of the site you want to visit. The "hostname" which is human-readable is only an alias for the cryptographic address, which corresponds to the base32 or base64. Without the cryptographic address, there is no way to access an I2P Site, this is by design. Distributing the address to people who do not know it yet is usually the responsibility of the Jump service provider. Visiting an I2P Site which is unknown will trigger the use of a Jump service. stats.i2p is the most reliable Jump service.</p>

<p>If you're hosting a site via i2ptunnel, then it won't have a registration with a jump service yet. To give it a URL locally, then visit the configuration page and click the button that says "Add to Local Address Book." Then go to http://127.0.0.1:7657/dns to look up the addresshelper URL and share it.</p>

<h3 id="ports"><span class="permalink"><a href="#ports">
What ports does I2P use?</a></span>
</h3>
<p>
The ports that are used by I2P can be divided into 2 sections: 
</p>

<ol>
  <li>Internet-facing ports, which are used for communication with other I2P routers</li>
  <li>Local ports, for local connections</li>
</ol>

<p>
These are described in detail below.
</p>

<ol>
  <li>Internet-facing ports<br> Note: Since release 0.7.8, new installs do not use port 8887; 
    a random port between 9000 and 31000 is selected when the program is run for the first time. 
    The selected port is shown on the router <a href="http://127.0.0.1:7657/confignet">configuration page</a>.<br>
    <b>OUTBOUND</b>
    <ul>
      <li>UDP from the random port listed on the <a href="http://127.0.0.1:7657/confignet">configuration page</a> to arbitrary remote UDP ports, allowing for replies</li>
      <li>TCP from random high ports to arbitrary remote TCP ports</li>
      <li>Outbound UDP on port 123, allowing for replies. 
        This is necessary for I2P's internal time sync (via SNTP - querying a random SNTP host in pool.ntp.org or another server you specify)</li>
    </ul>
    <b>INBOUND</b>
    <ul>
      <li>(Optional, recommended) UDP to the port noted on the <a href="http://127.0.0.1:7657/confignet">configuration page</a> from arbitrary locations</li>
      <li>(Optional, recommended) TCP to the port noted on <a href="http://127.0.0.1:7657/confignet">configuration page</a> from arbitrary locations</li>
      <li>Inbound TCP can be disabled on the <a href="http://127.0.0.1:7657/confignet">configuration page</a></li>
    </ul>
  </li>
  <li>Local I2P ports, listening only to local connections by default, except where noted:<br>
    <table class="table table-striped table-bordered">
      <tr>
        <th>
          PORT
        </th>
        <th>
          PURPOSE
        </th>
        <th>
          DESCRIPTION
        </th>
      </tr>
      <tr>
        <td>
          1900
        </td>
        <td>
          UPnP SSDP UDP multicast listener
        </td>
        <td>
          Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.
        </td>
      </tr>
      <tr>
        <td>
          2827
        </td>
        <td>
          BOB bridge
        </td>
        <td>
          A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. 
          May be changed in the bob.config file.
        </td>
      </tr>
      <tr>
        <td>
          4444
        </td>
        <td>
          HTTP proxy
        </td>
        <td>
          Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it 
          and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. 
          Include in your browser's proxy configuration for HTTP
        </td>
      </tr>
      <tr>
        <td>
          4445
        </td>
        <td>
          HTTPS proxy
        </td>
        <td>
          Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it 
          and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. 
          Include in your browser's proxy configuration for HTTPS
        </td>
      </tr>
      <tr>
        <td>
          6668
        </td>
        <td>
          IRC proxy
        </td>
        <td>
          A tunnel to the inside-the-I2P IRC network. 
          Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>
        </td>
      </tr>
      <tr>
        <td>
          7654
        </td>
        <td>
          I2CP (client protocol) port
        </td>
        <td>
          For advanced client usage. Do not expose to an external network.
        </td>
      </tr>
      <tr>
        <td>
          7656
        </td>
        <td>
          SAM bridge
        </td>
        <td>
          A socket API for clients. Disabled by default. May be enabled/disabled 
          on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on 
          <a href="http://127.0.0.1:7657/sam">sam</a>.
        </td>
      </tr>
      <tr>
        <td>
          7657 (or 7658 via SSL)
        </td>
        <td>
          Router console
        </td>
        <td>
          The router console provides valuable information about your router and the 
          network, in addition to giving you access to configure your router and its associated applications.
        </td>
      </tr>
      <tr>
        <td>
          7659
        </td>
        <td>
          'eepsite' - an example webserver (Jetty)
        </td>
        <td>
          Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is
          available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>
        </td>
      </tr>
      <tr>
        <td>
          7660
        </td>
        <td>
          I2PTunnel UDP port for SSH
        </td>
        <td>
          Required for Grizzled's/novg's UDP support. Instances disabled
          by default. May be enabled/disabled and configured to use a different 
          port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.
        </td>
      </tr>
      <tr>
        <td>
          123
        </td>
        <td>
          NTP Port
        </td>
        <td>
          Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.
        </td>
      </tr>
    </table>
    </li>
</ol>

<h3 id="subscriptions"><span class="permalink"><a href="#subscriptions">
I'm missing lots of hosts in my address book. What are some good subscription links?</a></span>
</h3>
<p>
The address book is located at <a href="http://localhost:7657/dns">http://localhost:7657/dns</a> where further information can be found.</p>
<ul>
  <li>What are some good address book subscription links?
    <p>You may try the following:</p>
<div class="links">
<ul>
<li><a href="http://stats.i2p/cgi-bin/newhosts.txt">http://stats.i2p/cgi-bin/newhosts.txt</a></li>
<li><a href="http://identiguy.i2p/hosts.txt">http://identiguy.i2p/hosts.txt</a></li>
</ul>
</div>
</ul>

<h3 id="remote_webconsole"><span class="permalink"><a href="#remote_webconsole">
How can I access the web console from my other machines or password protect it?</a></span>
</h3>
<p>
For security purposes, the router's admin console by default only listens for connections on the local interface.  

There are two methods for accessing the console remotely:</p>

<ol>
  <li>SSH Tunnel</li>
  <li>Configuring your console to be available on a Public IP address with a username &amp; password</li>
  </ol>
<p>These are detailed below:</p>

<ol>
  <li>SSH Tunnel<br>
      If you are running a Unix-like Operating System, this is the easiest method for remotely accessing your I2P console. 
      (Note: SSH server software is available for systems running Windows, for example <a href="https://github.com/PowerShell/Win32-OpenSSH">https://github.com/PowerShell/Win32-OpenSSH</a>)<br>
      Once you have configured SSH access to your system, the '-L' flag is passed to SSH with appropriate arguments - for example:
      <code>
        <pre>
        ssh -L 7657:localhost:7657 (System_IP)
        </pre>
      </code>
      where '(System_IP)' is replaced with your System's IP address. 
      This command forwards port 7657 (the number before the first colon) to the remote system's (as specified by the string 'localhost' between the first and second colons) port 7657 (the number after the second colon). 
      Your remote I2P console will now be available on your local system as 'http://localhost:7657' and will be available for as long as your SSH session is active. 
      If you would like to start an SSH session without initiating a shell on the remote system, you can add the '-N' flag:
      <code>
        <pre>
        ssh -NL 7657:localhost:7657 (System_IP)
        </pre>
      </code>
  </li>
  <li>Configuring your console to be available on a Public IP address with a username &amp; password<br>
    <ol>
      <li>Open <code>~/.i2p/clients.config</code> and replace
        <code>
          <pre>
                clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
          </pre>
        </code>
              with
        <code>
          <pre>
                clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
          </pre>
        </code>
              where you replace (System_IP) with your system's public IP
              address</li>
      <li>Go to <a href="http://localhost:7657/configui">http://localhost:7657/configui</a> and add a console username and password if desired - 
        Adding a username &amp; password is highly recommended to secure your I2P console from tampering, which could lead to de-anonymization.</li>
      <li>Go to <a href="http://localhost:7657/index">http://localhost:7657/index</a> and hit "Graceful restart", 
        which restarts the JVM and reloads the client applications</li>
    </ol>
      After that fires up, you should now be able to reach your console remotely. 
      Load the router console at <code>http://(System_IP):7657</code> and you will be prompted for the username and password you specified in step 2 above if your browser supports the authentication popup.
      <br>
      NOTE: You can specify 0.0.0.0 in the above configuration. 
      This specifies an interface, not a network or netmask. 
      0.0.0.0 means "bind to all interfaces", so it can be reachable on 127.0.0.1:7657 as well as any LAN/WAN IP. 
      Be careful when using this option as the console will be available on ALL addresses configured on your system.</li>
</ol>

<h3 id="remote_i2cp"><span class="permalink"><a href="#remote_i2cp">
How can I use applications from my other machines?</a></span>
</h3>
<p>
Please see the previous answer for instructions on using SSH Port Forwarding, and also see this page in your console: 
<a href="http://localhost:7657/configi2cp">http://localhost:7657/configi2cp</a>
</p>

<h3 id="socks"><span class="permalink"><a href="#socks">
Is it possible to use I2P as a SOCKS proxy?</a></span>
</h3>
<p>
The SOCKS proxy has been functional since release 0.7.1. SOCKS 4/4a/5 are supported. 
I2P does not have a SOCKS outproxy so it is limited to use within I2P only.
</p>
<p>
Many applications leak sensitive information that could identify you on the Internet and this is a risk that one should be aware of when using the I2P SOCKS proxy. 
I2P only filters connection data, but if the program you intend to run sends this information as content, I2P has no way to protect your anonymity. 
For example, some mail applications will send the IP address of the machine they are running on to a mail server. 
We recommend I2P-specific tools or applications (such as <a href="http://localhost:7657/i2psnark/">I2PSnark</a> for torrents), or applications that are known to be safe to use with I2P that include popular plugins found on <a href="https://www.mozilla.org/">Firefox</a>.
</p>

<h3 id="proxy_other"><span class="permalink"><a href="#proxy_other">
How do I access IRC, BitTorrent, or other services on the regular Internet?</a></span>
</h3>
<p>
There are services called Outproxies that bridge between I2P and the Internet, like Tor Exit Nodes. Default outproxy functionality for HTTP and HTTPS is provided by <code>exit.stormycloud.i2p</code> and is run by StormyCloud Inc. It is configured in the HTTP Proxy. 
Additionally, to help protect anonymity, I2P does not permit you to make anonymous connections to the regular Internet by default. 
Please see the <a href="/docs/api/socks#outproxy">Socks Outproxy</a> page for more information.
</p>

<h2>Reseeds</h2>

<h3 id="reseed"><span class="permalink"><a href="#reseed">
My router has been up for several minutes and has zero or very few connections</a></span>
</h3>
<p>
First check the <a href="http://127.0.0.1:7657/netdb">http://127.0.0.1:7657/netdb</a> page in the Router Console &ndash; your network database. 
If you do not see a single router listed from within I2P but the console says you should be firewalled, then you probably cannot connect to the reseed servers. 
If you do see other I2P routers listed then try to lower the number of max connections <a href="http://127.0.0.1:7657/config">http://127.0.0.1:7657/config</a> maybe your router cannot handle many connections.
</p>

<h3 id="manual_reseed"><span class="permalink"><a href="#manual_reseed">
How do I reseed manually?</a></span>
</h3>
<p>
Under normal circumstances, I2P will connect you to the network automatically using our bootstrap links. If disrupted internet makes bootstrapping from reseed servers fail, an easy way to bootstrap is by using Tor browser(By default it open localhost), which
works very nicely with <a href="http://127.0.0.1:7657/configreseed">http://127.0.0.1:7657/configreseed</a>. 
It is also possible to reseed an I2P router manually.</p>
<p>
When using Tor browser to reseed you can select multiple URLs at once and proceed. Though the default value which is 2(out of the multiple urls) will also work but it will be slow.
</p>

<h2>Privacy-Safety</h2>

<h3 id="exit"><span class="permalink"><a href="#exit">
Is my router an "exit node"(outproxy) to the regular Internet? I don't want it to be.</a></span>
</h3>
<p>
No, your router participates in the transport of encrypted e2e traffic across the i2p network to a random tunnel endpoint, usually not an outproxy, but no traffic is passed between your router and the Internet over the transport layer. <br>
As an end-user, you should not run an outproxy if you are not skilled in system and network administration.
</p>

<h3 id="detection"><span class="permalink"><a href="#detection">
Is it easy to detect the use of I2P by analyzing network traffic?</a></span>
</h3>
<p>
I2P traffic usually looks like UDP traffic, and not much more &ndash; and making it look like not that much more is a goal. It also supports TCP. 
With some effort, passive traffic analysis may be able to classify the traffic as "I2P", but we hope that the continued development of traffic obfuscation will reduce this further. 
Even a fairly simple protocol obfuscation layer like obfs4 will prevent censors from blocking I2P (it is a goal that I2P deploys).
</p>

<h3 id="safe"><span class="permalink"><a href="#safe">
Is using I2P Safe?</a></span>
</h3>
<p>
It depends on your personal threat model. For most people, I2P is way safer than not using any protection. Some other networks (like Tor, mixminion/mixmaster), are probably safer against certain adversaries. 
For example, I2P traffic does not use TLS/SSL, so it does not have the "weakest link" issues that Tor does. 
I2P was used by a lot of people in Syria at the &#34;Arab spring&#34;, and recently the project has seen bigger growth in smaller linguistical installations of I2P in the near- and middle east. 
The most important thing to note here is that I2P is a technology and you need a how-to/guide to enhance your privacy/anonymity on the Internet. 
Also check your browser or import the fingerprint-search-engine to block fingerprint attacks with a very big (meaning: typical long tails / very accurate diverse data structure) dataset about lot of environment things and dnnt use VPN to reduce all risk comes from it self like the own TLS cache behaviour and the technical construction of the provider business that can be hacked easier as a own desktop system. 
May using a isolated tor V-Browser with its great anti-fingerprint protections and an overall appguard-livetime-protection with only allow for the necessary systems communications and a last standing vm-use with anti-spy disable scripts and live-cd to remove any "almost permanent possible risk" and down all risks by a decreasing prpbability are a good option in public network and top individual risk model and might be the best you can do with this goal for i2p use. 

</p>

<h3 id="netdb_ip"><span class="permalink"><a href="#netdb_ip">
I see IP addresses of all other I2P nodes in the router console. Does that mean my IP address is visible by others?</a></span>
</h3>
<p>
Yes, for other I2P nodes who know about your router. We use this to connect with the rest of the I2P network. 
The addresses are physically located in "routerInfos (key,value)objects", either remotely fetched or received from peer. 
The "routerInfos" holds some information (some optional opportunistic added), "published by peer", about the router itself for bootstrapping. 
No data is in this object about clients. 
Looking closer under the hood will tell you that everybody got counted with the newest type of creating ids called "SHA-256 Hashes (low=Positive hash(-key), high=Negative hash(+key))". 
The I2P network got a own database datas of routerInfos created during upload and indexing, but this depends deep into the realization of the key/value tables and networks topology and state-of-load / state-of-bandwidth and routing probabilities for storages in DB components.
</p>

<h3 id="proxy_safe"><span class="permalink"><a href="#proxy_safe">
Is using an outproxy safe?</a></span>
</h3>
<p>
It depends on what your definition of "safe" is. Outproxies are great when they work, but unfortunately they voluntary run by people who may lose interest or may not have the resources to maintain them 24/7 – please be aware that you may experience periods of time during which services are unavailable, interrupted, or unreliable, and we are not associated with this service and have no influence on it.
</p>
<p>
The outproxys themselves can see your traffic come and go, with the exception of end-to-end encrypted HTTPS/SSL data, just like your ISP can see your traffic come and go from your computer. If you are comfortable with your ISP, it wouldn't be any worse with the outproxy.
</p>

<h3 id="deanon"><span class="permalink"><a href="#deanon">
What about "De-Anonymizing" attacks?</a></span>
</h3>
<p>
For a very long explanation, read more at our articles about <a href="/docs/overview/threat-model"> Threat Model</a>. 
In general, de-anonymizing is not trivial, but possible if you are not cautious enough.
</p>

<h2>Internet Access/Performance</h2>

<h3 id="outproxy"><span class="permalink"><a href="#outproxy">
I can't access regular Internet sites through I2P.</a></span>
</h3>
<p>
Proxying to Internet sites (eepsites that are out to the Internet) is provided as a service to I2P users by non-block providers. 
This service is not the main focus of I2P development, and is provided on a voluntary basis. 
Eepsites that are hosted on I2P should always work without an outproxy. 
Outproxies are a convenience but they are by design not perfect nor a large part of the project. 
Be aware that they may not be able to provide the high-quality service other services of I2P may provide.
</p>

<h3 id="https"><span class="permalink"><a href="#https">
I can't access https:// or ftp:// sites through I2P.</a></span>
</h3>
<p>
The default HTTP proxy supports HTTP and HTTPS outproxying only.
</p>

<h3 id="cpu"><span class="permalink"><a href="#cpu">
Why is my router using too much CPU?</a></span>
</h3>
<p>
First, make sure you have the latest version of every I2P related part – older versions had<br>
unnecessary cpu-eating sections in code.
<br>There is also a <a href="/about/performance">performance Log</a> that documents some of the improvements in I2P performance over time.
</p>

<h3 id="vary"><span class="permalink"><a href="#vary">
My active peers / known peers / participating tunnels / connections / bandwidth vary dramatically over time! Is anything wrong?</a></span>
</h3>
<p>
The general stability of the I2P network is an ongoing area of research. A particular amount of that research is focused on how small changes to configuration settings change the behavior of the router. 
As I2P is a peer-to-peer network, the actions by other peers will have an influence on your router's performance.
</p>

<h3 id="slow"><span class="permalink"><a href="#slow">
What makes downloads, torrents, web browsing, and everything else slower on I2P as compared to the regular internet?</a></span>
</h3>
<p>
I2P has different protections that add extra routing and additional layers of encryption. It also bounces traffic through other peers(Tunnels) that have their own speed and quality, some are slow, some fast. 
This adds up to lots of overhead and traffic at different paces in different directions. 
By design all these things will make it slower compared to a direct connection on the internet, but much more anonymous and still fast enough for most things.
</p>

<p>
Below is an example presented with an explanation to help provide some context to the latency and bandwidth considerations when using I2P.
</p>
<p>
Consider the diagram below. It depicts a connection between a client making a request via I2P, a server receiving the request via I2P and then responding back via I2P as well. The circuit the request travels upon is also depicted.
</p>
<p>
From the diagram, consider that the boxes labelled 'P', 'Q' and 'R' represent an outbound tunnel for 'A' and that the boxes labelled 'X', 'Y' and 'Z' repres
ent an outbound tunnel for 'B'. 
Similarly, the boxes labelled 'X', 'Y' and 'Z' represent and inbound tunnel for 'B' while the boxes labelled 'P_1', 'Q_1' and 'R_1' represent an inbound tunnel for 'A'. 
The arrows in between the boxes show the direction of traffic. 
The text above and below the arrows detail some example bandwidth between a pair of hops as well as example latencies.
</p>

<p>
When both client and server are using 3-hop tunnels throughout, a total of 12 other I2P routers are involved in relaying traffic. 
6 peers relay traffic from the client to the server which is split into a 3-hop outbound tunnel from 'A' ('P', 'Q', 'R') and a 3-hop inbound tunnel to 'B' ('X', 'Y', 'Z').  
Similarly, 6 peers relay traffic from the server to back to the client.
</p>

<p>
First, we can consider latency - the time that it takes for a request from a client to traverse the I2P network, reach the the server and traverse back to the client. 
Adding up all latencies we see that:
</p>

<code>
<pre>
      40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
    + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client) 
    -----------------------------------
    TOTAL:                          740 ms
</pre>
</code>

<p>
The total round-trip time in our example adds up to 740 ms - certainly much higher than what one would normally see while browsing regular internet websites.
</p>

<p>
Second, we can consider available bandwidth. 
This is determined through the slowest link between hops from the client and server as well as when traffic is being transmitted by the server to the client. 
For traffic going from the client to the server, we see that the available bandwidth in our example between hops 'R' &amp; 'X' as well as hops 'X' &amp; 'Y' is 32 KB/s. 
Despite higher available bandwidth between the other hops, these hops will act as a bottleneck and will limit the maximum available bandwidth for traffic from 'A' to 'B' at 32 KB/s. 
Similarly, tracing the path from server to client shows that there is maximum bandwidth of 64 KB/s - between hops 'Z_1' &amp; 'Y_1, 'Y_1' &amp; 'X_1' and 'Q_1' &amp; 'P_1'.
</p>

<p>
We recommend increasing your bandwidth limits. 
This helps the network by increasing the amount of available bandwidth which will in turn improve your I2P experience. 
Bandwidth settings are located on the <a href="http://localhost:7657/config">http://localhost:7657/config</a> page. 
Please be aware of your internet connection's limits as determined by your ISP, and adjust your settings accordingly. 
</p>

<p>
We also recommend setting a sufficient amount of shared bandwidth - this allows for participating tunnels to be routed through your I2P router. 
Allowing participating traffic keeps your router well-integrated in the network and improves your transfer speeds.
</p>

<p>
I2P is a work in progress. Lots of improvements and fixes are being implemented, and, generally speaking, running the latest release will help your performance.
If you haven't, <a href="">install the latest release</a>.
</p>

<h3 id="bug"><span class="permalink"><a href="#bug">
I think I found a bug, where can I report it?</a></span></h3>

<p>
You may report any bugs/issues that you encounter on our bugtracker, which is available over both non-private internet and I2P. 
We have a discussion forum, also available on I2P and non-private internet. You can join our IRC channel as well: 
either through our IRC network, IRC2P, or on Freenode.</p>

<ul>
<li>Our Bugtracker:
  <ul>
    <li>Non-private internet: <a href="https://i2pgit.org/I2P_Developers/i2p.i2p/issues">https://i2pgit.org/I2P_Developers/i2p.i2p/issues</a></li>
    <li>On I2P: <a href="http://git.idk.i2p/I2P_Developers/i2p.i2p/issues">http://git.idk.i2p/I2P_Developers/i2p.i2p/issues</a></li>
  </ul>
<li>Our forums: <a href="http://i2pforum.i2p/">i2pforum.i2p</a></li>
<li>You may paste any interesting logs to a paste service such as the non-private internet services listed on the 
  <a href="https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory">PrivateBin Wiki</a>, or an I2P paste service such as this 
  <a href="http://paste.crypthost.i2p">PrivateBin instance</a> or this 
  <a href="http://pasta-nojs.i2p">Javascript-free paste service</a> and follow up on IRC in #i2p</li>
<li>
Join #i2p-dev Discuss with the developers on IRC
</li></ul>

<p>
Please include relevant information from the router logs page which is available at: 
<a href="http://127.0.0.1:7657/logs">http://127.0.0.1:7657/logs</a>.
We request that you share all of the text under the 'I2P Version and Running Environment' 
section as well as any errors or warnings displayed in the various logs displayed on the page.
</p>

<hr />

<h3 id="question"><span class="permalink"><a href="#question">
I have a question!</a></span>
</h3>
<p>
Great! Find us on IRC:
<ul>
  <li>on <code>irc.freenode.net</code> channel <code>#i2p</code></li>
  <li>on <code>IRC2P</code> channel <code>#i2p</code></li>
</ul>
or post to <a href="http://i2pforum.i2p/">the forum</a> and we'll post it here (with the answer, hopefully).
</p>
