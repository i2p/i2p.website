---
title: "कॉन्फ़िगरेशन फाइल विनिर्देश"
description: "राउटर और एप्लिकेशनों द्वारा उपयोग की जाने वाली I2P कॉन्फ़िगरेशन फ़ाइलों का विनिर्देश"
slug: "configuration"
aliases:
  - "/hi/configuration"
  - "/hi/configuration/"
category: "प्रारूप"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## अवलोकन

यह पृष्ठ I2P कॉन्फ़िगरेशन फाइलों का एक सामान्य विनिर्देश प्रदान करता है, जो router और विभिन्न अनुप्रयोगों द्वारा उपयोग की जाती हैं। यह विभिन्न फाइलों में निहित जानकारी का अवलोकन भी देता है, और जहां उपलब्ध है वहां विस्तृत दस्तावेज़ीकरण के लिंक प्रदान करता है।

## सामान्य प्रारूप

एक I2P कॉन्फ़िगरेशन फ़ाइल Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) के अनुसार फॉर्मेट की जाती है, निम्नलिखित अपवादों के साथ:

- Encoding UTF-8 होनी चाहिए
- कोई escapes का उपयोग नहीं करता या पहचानता नहीं, `\` सहित, इसलिए lines को continue नहीं किया जा सकता
- `#` या `;` comment शुरू करता है, लेकिन `!` नहीं करता
- `#` किसी भी position में comment शुरू करता है लेकिन `;` को comment शुरू करने के लिए column 1 में होना चाहिए
- Keys पर leading और trailing whitespace को trim नहीं किया जाता
- Values पर leading और trailing whitespace को trim किया जाता है
- `=` ही एकमात्र key-termination character है (`:` या whitespace नहीं)
- `=` के बिना वाली lines को ignore किया जाता है। Release 0.9.10 के बाद से, "" value वाली keys को support किया जाता है।
- चूंकि कोई escapes नहीं हैं, keys में `#`, `=`, या `\n` नहीं हो सकता, या `;` से शुरू नहीं हो सकता
- चूंकि कोई escapes नहीं हैं, values में `#` या `\n` नहीं हो सकता, या `\r` या whitespace से शुरू या समाप्त नहीं हो सकता

फ़ाइल को क्रमबद्ध करना आवश्यक नहीं है, लेकिन अधिकांश एप्लिकेशन फ़ाइल में लिखते समय key के अनुसार क्रमबद्ध करते हैं, ताकि पढ़ने और मैन्युअल संपादन में आसानी हो।

Reads और writes को DataHelper loadProps() और storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html) में implement किया गया है। ध्यान दें कि file format, [Mapping](/docs/specs/common-structures/#type-mapping) में निर्दिष्ट I2P protocols के लिए serialized format से काफी अलग है।

## मुख्य लाइब्रेरी और router

### क्लाइंट्स (clients.config)

router console में /configclients के माध्यम से कॉन्फ़िगर किया जाता है। रिलीज़ 0.9.42 के बाद से, डिफ़ॉल्ट clients.config फाइल को clients.config.d डायरेक्टरी में प्रत्येक क्लाइंट के लिए अलग-अलग कॉन्फ़िगरेशन फाइलों में विभाजित किया गया है। विभाजन के बाद, व्यक्तिगत फाइलों में गुण "clientApp.0." के साथ prefixed होते हैं।

प्रारूप निम्नलिखित है:

लाइनें `clientApp.x.prop=val` के रूप में होती हैं, जहां x ऐप नंबर है। ऐप नंबर 0 से शुरू होने चाहिए और लगातार होने चाहिए।

गुण निम्नलिखित हैं:

**main** : पूरा class नाम। आवश्यक। : इस class में constructor या main() method चलाया जाएगा, यह इस बात पर निर्भर करता है कि client managed है या unmanaged। विवरण के लिए नीचे देखें।

**name** : कंसोल पर प्रदर्शित होने वाला नाम।

**args** : मुख्य क्लास के लिए तर्क, स्पेस या टैब द्वारा अलग किए गए। स्पेस या टैब वाले तर्कों को `'` या `"` के साथ उद्धृत किया जा सकता है

**delay** : शुरू करने से पहले सेकंड, डिफ़ॉल्ट 120

**onBoot** : `{true|false}` : डिफ़ॉल्ट false, 0 की देरी को बाध्य करता है, delay सेटिंग को ओवरराइड करता है

**startOnLoad** : `{true|false}` : क्या क्लाइंट को बिल्कुल चलाना है? डिफ़ॉल्ट true

निम्नलिखित अतिरिक्त गुण केवल plugins द्वारा उपयोग किए जाते हैं:

**stopargs** : क्लाइंट को रोकने के लिए आर्गुमेंट्स।

**uninstallargs** : क्लाइंट को अनइंस्टॉल करने के लिए आर्गुमेंट्स।

**classpath** : क्लाइंट के लिए अतिरिक्त classpath तत्व, कॉमा द्वारा अलग किए गए।

निम्नलिखित प्रतिस्थापन args, stopargs, uninstallargs, और classpath लाइनों में किए जाते हैं, केवल plugins के लिए:

**$I2P** : आधार I2P स्थापना निर्देशिका

**$CONFIG** : उपयोगकर्ता की कॉन्फ़िगरेशन डायरेक्टरी (जैसे ~/.i2p)

**$PLUGIN** : इस plugin की directory (उदाहरण के लिए ~/.i2p/plugins/foo)

**$OS** : ऑपरेटिंग सिस्टम का नाम (जैसे "linux")

**$ARCH** : आर्किटेक्चर का नाम (जैसे "amd64")

"main" को छोड़कर सभी properties वैकल्पिक हैं। `#` से शुरू होने वाली लाइनें comments हैं।

यदि विलंब शून्य से कम है, तो client router के RUNNING अवस्था तक पहुंचने तक प्रतीक्षा करेगा और फिर एक नए thread में तुरंत शुरू हो जाएगा।

यदि विलंब शून्य के बराबर है, तो client तुरंत चलाया जाता है, उसी thread में, ताकि exceptions को console में प्रचारित किया जा सके। इस स्थिति में, client को या तो एक exception throw करना चाहिए, जल्दी return करना चाहिए, या अपना स्वयं का thread spawn करना चाहिए।

यदि विलंब शून्य से अधिक है, तो यह एक नए thread में चलाया जाएगा, और exceptions को लॉग किया जाएगा लेकिन console में प्रसारित नहीं किया जाएगा।

क्लाइंट्स "managed" या "unmanaged" हो सकते हैं।

### लॉगर (logger.config)

Router console में /configlogging के माध्यम से कॉन्फ़िगर किया गया।

गुण इस प्रकार हैं:

```
# Default 20
logger.consoleBufferSize=n
# Default from locale; format as specified by Java SimpleDateFormat
logger.dateFormat=HH:mm:ss.SSS
# Default ERROR
logger.defaultLevel=CRIT|ERROR|WARN|INFO|DEBUG
# Default true
logger.displayOnScreen=true|false
# Default true
logger.dropDuplicates=true|false
# Default false
logger.dropOnOverflow=true|false
# As of 0.9.18. Default 29 (seconds)
logger.flushInterval=nnn
# d = date, c = class, t = thread name, p = priority, m = message
logger.format={dctpm}*
# As of 0.9.56. Default false
logger.gzip=true|false
# Max to buffer before flushing. Default 1024
logger.logBufferSize=n
# Default logs/log-@.txt; @ replaced with number
logger.logFileName=name
logger.logFilenameOverride=name
# Default 10M
logger.logFileSize=nnn[K|M|G]
# Highest file number. Default 2
logger.logRotationLimit=n
# As of 0.9.56. Default 65536 (bytes)
logger.minGzipSize=nnnnn
# Default CRIT
logger.minimumOnScreenLevel=CRIT|ERROR|WARN|INFO|DEBUG
logger.record.{class}=CRIT|ERROR|WARN|INFO|DEBUG
```
### व्यक्तिगत Plugin (plugins/*/plugin.config)

[प्लगइन विनिर्देश](/docs/specs/plugin) देखें। ध्यान दें कि प्लगइन्स में clients.config, i2ptunnel.config, और webapps.config फाइलें भी हो सकती हैं।

### प्लगइन्स (plugins.config)

प्रत्येक स्थापित plugin के लिए सक्षम/अक्षम करें।

गुण निम्नलिखित हैं:

```
plugin.{name}.startOnLoad=true|false
```
### वेबऐप्स (webapps.config)

प्रत्येक स्थापित webapp के लिए सक्षम/अक्षम करें।

गुण निम्नलिखित हैं:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

router console में /configadvanced के माध्यम से कॉन्फ़िगर किया गया।

## एप्लिकेशन्स

### एड्रेसबुक (addressbook/config.txt)

SusiDNS में दस्तावेज़ देखें।

### I2PSnark (i2psnark.config.d/i2psnark.config)

एप्लिकेशन GUI के माध्यम से कॉन्फ़िगर किया गया।

### व्यक्तिगत i2psnark (i2psnark.config.d/*/*.config)

किसी व्यक्तिगत torrent के लिए कॉन्फ़िगरेशन। एप्लिकेशन gui के माध्यम से कॉन्फ़िगर किया जाता है।

### I2PTunnel (i2ptunnel.config)

router console में /i2ptunnel एप्लिकेशन के माध्यम से कॉन्फ़िगर किया जाता है। रिलीज़ 0.9.42 के अनुसार, डिफ़ॉल्ट i2ptunnel.config फ़ाइल को i2ptunnel.config.d डायरेक्टरी में प्रत्येक tunnel के लिए अलग-अलग कॉन्फ़िगरेशन फ़ाइलों में विभाजित किया गया है। विभाजन के बाद, अलग-अलग फ़ाइलों में properties के साथ "tunnel.N." का prefix नहीं लगाया जाता है।

नोट: "tunnel.N.option.i2cp.*" विकल्प, I2CP विकल्प प्रतीत होने के बावजूद, i2ptunnel में कार्यान्वित हैं, और I2CP या SAM जैसे अन्य इंटरफेसेस या APIs के माध्यम से समर्थित नहीं हैं।

गुण निम्नलिखित हैं:

```
# Display description for UI
tunnel.N.description=

# Router IP address or host name. Ignored if in router context.
tunnel.N.i2cpHost=127.0.0.1

# Router I2CP port. Ignored if in router context.
tunnel.N.i2cpPort=nnnn

# For clients only. Local listen IP address or host name.
tunnel.N.interface=127.0.0.1

# For clients only. Local listen port.
tunnel.N.listenPort=nnnn

# Display name for UI
tunnel.N.name=

# Servers only. Default false. Originate connections to local server with a
# unique IP per-remote-destination.
tunnel.N.option.enableUniqueLocal=true|false

# Clients only. Do not open the socket manager and build tunnels
# until the first socket is opened on the local port.
# Default false
tunnel.N.option.i2cp.delayOpen=true|false

# Servers only. Persistent private leaseset key
tunnel.N.option.i2cp.leaseSetPrivateKey=base64

# Servers only. Persistent private leaseset key
tunnel.N.option.i2cp.leaseSetSigningPrivateKey=sigtype:base64

# Clients only. Create a new destination when reopening the socket manager,
# after it was previously closed due to an idle timeout.
# Default false
# When true, requires I2CP option i2cp.closeOnIdle=true
# When true, tunnel.N.option.persistentClientKey must be unset or false
tunnel.N.option.i2cp.newDestOnResume=true|false

# Servers only. The maximum size of the thread pool, default 65. Ignored
# for standard servers.
tunnel.N.option.i2ptunnel.blockingHandlerCount=nnn

# HTTP client only. Whether to use allow SSL connections to i2p addresses.
# Default false.
tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL=true|false

# HTTP client only. Whether to disable address helper links. Default false.
tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper=true|false

# HTTP client only. Comma- or space-separated list of jump server URLs.
tunnel.N.option.i2ptunnel.httpclient.jumpServers=http://example.i2p/jump

# HTTP client only. Whether to pass Accept* headers through. Default false.
# Note: Does not affect "Accept" and "Accept-Encoding".
tunnel.N.option.i2ptunnel.httpclient.sendAccept=true|false

# HTTP client only. Whether to pass Referer headers through. Default false.
tunnel.N.option.i2ptunnel.httpclient.sendReferer=true|false

# HTTP client only. Whether to pass User-Agent headers through. Default
# false.
tunnel.N.option.i2ptunnel.httpclient.sendUserAgent=true|false

# HTTP client only. Whether to pass Via headers through. Default false.
tunnel.N.option.i2ptunnel.httpclient.sendVia=true|false

# HTTP client only. Comma- or space-separated list of in-network SSL
# outproxies.
tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies=example.i2p

# SOCKS client only. Comma- or space-separated list of in-network
# outproxies for any ports not specified.
tunnel.N.option.i2ptunnel.socks.proxy.default=example.i2p

# SOCKS client only. Comma- or space-separated list of in-network
# outproxies for port NNNN.
tunnel.N.option.i2ptunnel.socks.proxy.NNNN=example.i2p

# HTTP client only. Whether to use a registered local outproxy plugin.
# Default true.
tunnel.N.option.i2ptunnel.useLocalOutproxy=true|false

# Servers only. Whether to use a thread pool. Default true. Ignored for
# standard servers, always false.
tunnel.N.option.i2ptunnel.usePool=true|false

# IRC Server only. Only used if fakeHostname contains a %c.  If unset,
# cloak with a random value that is persistent for the life of this tunnel.
# If set, cloak with the hash of this passphrase.  Use to have consistent
# mangling across restarts, or for multiple IRC servers cloak consistently
# to be able to track users even when they switch servers.  Note: don't
# quote or put spaces in the passphrase, the i2ptunnel gui can't handle it.
tunnel.N.option.ircserver.cloakKey=

# IRC Server only. Set the fake hostname sent by I2PTunnel, %f is the full
# B32 destination hash, %c is the cloaked hash.
tunnel.N.option.ircserver.fakeHostname=%f.b32.i2p

# IRC Server only. Default user.
tunnel.N.option.ircserver.method=user|webirc

# IRC Server only. The password to use for the webirc protocol.  Note:
# don't quote or put spaces in the passphrase, the i2ptunnel gui can't
# handle it.
tunnel.N.option.ircserver.webircPassword=

# IRC Server only.
tunnel.N.option.ircserver.webircSpoofIP=

# For clients only. Alias for the private key in the keystore for the SSL
# socket. Will be autogenerated if a new key is created.
tunnel.N.option.keyAlias=

# For clients only. Password for the private key for the SSL socket. Will be
# autogenerated if a new key is created.
tunnel.N.option.keyPassword=

# For clients only. Path to the keystore file containing the private key for
# the SSL socket. Will be autogenerated if a new keystore is created.
# Relative to $(I2P_CONFIG_DIR)/keystore/ if not absolute.
tunnel.N.option.keystoreFile=i2ptunnel-(random string).ks

# For clients only. Password for the keystore containing the private key for
# the SSL socket. Default is "changeit".
tunnel.N.option.keystorePassword=changeit

# HTTP Server only. Max number of POSTs allowed for one destination per
# postCheckTime. Default 0 (unlimited)
tunnel.N.option.maxPosts=nnn

# HTTP Server only. Max number of POSTs allowed for all destinations per
# postCheckTime. Default 0 (unlimited)
tunnel.N.option.maxTotalPosts=nnn

# HTTP Clients only. Whether to send authorization to an outproxy. Default
# false.
tunnel.N.option.outproxyAuth=true|false

# HTTP Clients only. The password for the outproxy authorization.
tunnel.N.option.outproxyPassword=

# HTTP Clients only. The username for the outproxy authorization.
tunnel.N.option.outproxyUsername=

# SOCKS client only. The type of the configured outproxies: socks or connect (HTTPS).
# Default socks. As of 0.9.57.
tunnel.N.option.outproxyType=socks|connect

# Clients only. Whether to store a destination in a private key file and
# reuse it. Default false.
# When true, tunnel.N.option.newDestOnResume must be unset or false
tunnel.N.option.persistentClientKey=true|false

# HTTP Server only. Time period for banning POSTs from a single destination
# after maxPosts is exceeded, in seconds. Default 1800 seconds.
tunnel.N.option.postBanTime=nnn

# HTTP Server only. Time period for checking maxPosts and maxTotalPosts, in
# seconds. Default 300 seconds.
tunnel.N.option.postCheckTime=nnn

# HTTP Server only. Time period for banning all POSTs after maxTotalPosts
# is exceeded, in seconds. Default 600 seconds.
tunnel.N.option.postTotalBanTime=nnn

# HTTP Clients only. Whether to require local authorization for the proxy.
# Default false. "true" is the same as "basic".
tunnel.N.option.proxyAuth=true|false|basic|digest

# HTTP Clients only. The MD5 of the password for local authorization for
# user USER.
tunnel.N.option.proxy.auth.USER.md5=(32 char lowercase hex)

# HTTP Clients only. The SHA-256 of the password for local authorization for
# user USER. (RFC 7616) Since 0.9.56
tunnel.N.option.proxy.auth.USER.sha256=(64 char lowercase hex)

# HTTP Servers only. Whether to reject incoming connections apparently via
# an inproxy. Default false.
tunnel.N.option.rejectInproxy=true|false

# HTTP Servers only. Whether to reject incoming connections containing a
# referer header. Default false. Since 0.9.25.
tunnel.N.option.rejectReferer=true|false

# HTTP Servers only. Whether to reject incoming connections containing
# specific user-agent headers. Default false. Since 0.9.25. See
# tunnel.N.option.userAgentRejectList
tunnel.N.option.rejectUserAgents=true|false

# Servers only. Overrides targetHost and targetPort for incoming port NNNN.
tunnel.N.option.targetForPort.NNNN=hostnameOrIP:nnnn

# HTTP Servers only. Comma-separated list of strings to match in the
# user-agent header. Since 0.9.25. Example: "Mozilla,Opera". Case-sensitive.
# As of 0.9.33, a string of "none" may be used to match an empty user-agent.
# See tunnel.N.option.rejectUserAgents
tunnel.N.option.userAgentRejectList=string1[,string2]*

# Default false. For servers, use SSL for connections to local server. For
# clients, SSL is required for connections from local clients.
tunnel.N.option.useSSL=false

# Each option is passed to I2CP and streaming with "tunnel.N.option."
# stripped off. See those docs.
tunnel.N.option.*=

# For servers and clients with persistent keys only. Absolute path or
# relative to config directory.
tunnel.N.privKeyFile=filename

# For proxies only. Comma- or space-separated host names.
tunnel.N.proxyList=example.i2p[,example2.i2p]

# For clients only. Default false.
tunnel.N.sharedClient=true|false

# For HTTP servers only. Host name to be passed to the local server in the
# HTTP headers.  Default is the base 32 hostname.
tunnel.N.spoofedHost=example.i2p

# For HTTP servers only. Host name to be passed to the local server in the
# HTTP headers.  Overrides above setting for incoming port NNNN, to allow
# virtual hosts.
tunnel.N.spoofedHost.NNNN=example.i2p

# Default true
tunnel.N.startOnLoad=true|false

# For clients only. Comma- or space-separated host names or host:port.
tunnel.N.targetDestination=example.i2p[:nnnn][,example2.i2p[:nnnn]]

# For servers only. Local IP address or host name to connect to.
tunnel.N.targetHost=

# For servers only. Port on targetHost to connect to.
tunnel.N.targetPort=nnnn

# The type of i2ptunnel
tunnel.N.type=client|connectclient|httpbidirserver|httpclient|httpserver|ircclient|ircserver|
          server|socksirctunnel|sockstunnel|streamrclient|streamrserver
```
नोट: प्रत्येक 'N' एक tunnel नंबर है जो 0 से शुरू होता है। नंबरिंग में कोई अंतराल नहीं हो सकता।

### Router Console

router console router.config फ़ाइल का उपयोग करता है।

### SusiMail (susimail.config)

zzz.i2p पर पोस्ट देखें।

## संदर्भ

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [मैपिंग](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
