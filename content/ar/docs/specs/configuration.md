---
title: "مواصفات ملف التكوين"
description: "مواصفات ملفات تكوين I2P المستخدمة من قبل router والتطبيقات"
slug: "configuration"
aliases:
  - "/ar/configuration"
  - "/ar/configuration/"
category: "التنسيقات"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## نظرة عامة

تقدم هذه الصفحة مواصفات عامة لملفات تكوين I2P، المستخدمة من قِبل الموجه router والتطبيقات المختلفة. كما تقدم نظرة عامة على المعلومات الموجودة في الملفات المختلفة، وروابط إلى الوثائق التفصيلية حيثما كانت متاحة.

## التنسيق العام

ملف تكوين I2P مُنسق كما هو محدد في Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) مع الاستثناءات التالية:

- يجب أن يكون التشفير UTF-8
- لا يستخدم أو يتعرف على أي رموز هروب، بما في ذلك `\`، لذا لا يمكن استكمال الأسطر
- `#` أو `;` يبدأ تعليقاً، ولكن `!` لا يفعل ذلك
- `#` يبدأ تعليقاً في أي موضع ولكن `;` يجب أن يكون في العمود الأول لبدء تعليق
- المسافات البيضاء في البداية والنهاية لا تُحذف من المفاتيح
- المسافات البيضاء في البداية والنهاية تُحذف من القيم
- `=` هو الرمز الوحيد لإنهاء المفتاح (وليس `:` أو المسافة البيضاء)
- الأسطر التي لا تحتوي على `=` يتم تجاهلها. اعتباراً من الإصدار 0.9.10، المفاتيح التي تحتوي على قيمة "" مدعومة.
- نظراً لعدم وجود رموز هروب، لا يمكن للمفاتيح أن تحتوي على `#`، `=`، أو `\n`، أو تبدأ بـ `;`
- نظراً لعدم وجود رموز هروب، لا يمكن للقيم أن تحتوي على `#` أو `\n`، أو تبدأ أو تنتهي بـ `\r` أو مسافة بيضاء

لا يحتاج الملف إلى أن يكون مرتباً، ولكن معظم التطبيقات تقوم بالترتيب حسب المفتاح عند الكتابة في الملف، لتسهيل القراءة والتحرير اليدوي.

يتم تنفيذ عمليات القراءة والكتابة في DataHelper loadProps() و storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html). لاحظ أن تنسيق الملف يختلف بشكل كبير عن التنسيق المسلسل لبروتوكولات I2P المحددة في [Mapping](/docs/specs/common-structures/#type-mapping).

## المكتبة الأساسية وال router

### العملاء (clients.config)

يتم التكوين عبر /configclients في وحدة تحكم router. اعتباراً من الإصدار 0.9.42، يتم تقسيم ملف clients.config الافتراضي إلى ملفات تكوين فردية لكل عميل في دليل clients.config.d. بعد التقسيم، يتم إضافة البادئة "clientApp.0." للخصائص في الملفات الفردية.

الصيغة كما يلي:

الأسطر لها الشكل `clientApp.x.prop=val`، حيث x هو رقم التطبيق. أرقام التطبيقات يجب أن تبدأ بـ 0 وتكون متتالية.

الخصائص هي كما يلي:

**main** : اسم الفئة الكامل. مطلوب. : سيتم تشغيل الباني أو دالة main() في هذه الفئة، اعتماداً على ما إذا كان العميل مُدار أم غير مُدار. انظر أدناه للتفاصيل.

**name** : الاسم الذي سيتم عرضه على وحدة التحكم.

**args** : المعاملات للفئة الرئيسية، مفصولة بمسافات أو علامات تبويب. المعاملات التي تحتوي على مسافات أو علامات تبويب يمكن وضعها بين علامتي اقتباس `'` أو `"`

**delay** : الثواني قبل البدء، الافتراضي 120

**onBoot** : `{true|false}` : افتراضي false، يفرض تأخير 0، يتجاهل إعداد التأخير

**startOnLoad** : `{true|false}` : هل سيتم تشغيل العميل على الإطلاق؟ القيمة الافتراضية true

الخصائص الإضافية التالية تُستخدم فقط بواسطة الإضافات:

**stopargs** : معاملات إيقاف العميل.

**uninstallargs** : المعاملات المطلوبة لإلغاء تثبيت العميل.

**classpath** : عناصر classpath إضافية للعميل، مفصولة بفواصل.

يتم إجراء البدائل التالية في سطور args و stopargs و uninstallargs و classpath، للإضافات فقط:

**$I2P** : دليل تثبيت I2P الأساسي

**$CONFIG** : دليل إعدادات المستخدم (مثل ~/.i2p)

**$PLUGIN** : دليل هذا المكون الإضافي (مثل ~/.i2p/plugins/foo)

**$OS** : اسم نظام التشغيل (مثل "linux")

**$ARCH** : اسم المعمارية (مثل "amd64")

جميع الخصائص اختيارية باستثناء "main". الأسطر التي تبدأ بـ `#` هي تعليقات.

إذا كان التأخير أقل من صفر، فسوف ينتظر العميل حتى يصل router إلى حالة RUNNING ثم يبدأ فوراً في thread جديد.

إذا كان التأخير يساوي صفر، يتم تشغيل العميل فوراً، في نفس الخيط، بحيث يمكن نشر الاستثناءات إلى وحدة التحكم. في هذه الحالة، يجب على العميل إما أن يرمي استثناءً، أو يعود بسرعة، أو ينشئ خيطه الخاص.

إذا كان التأخير أكبر من الصفر، فسيتم تشغيله في thread جديد، وسيتم تسجيل الاستثناءات ولكن لن يتم نشرها إلى وحدة التحكم.

يمكن أن تكون العملاء "مُدارة" أو "غير مُدارة".

### المسجل (logger.config)

يتم تكوينه عبر /configlogging في وحدة تحكم الموجه.

الخصائص كما يلي:

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
### إضافة فردية (plugins/*/plugin.config)

انظر [مواصفات البرنامج المساعد](/docs/specs/plugin). لاحظ أن البرامج المساعدة قد تحتوي أيضاً على ملفات clients.config و i2ptunnel.config و webapps.config.

### الإضافات (plugins.config)

تمكين/تعطيل لكل إضافة مُثبتة.

الخصائص كما يلي:

```
plugin.{name}.startOnLoad=true|false
```
### تطبيقات الويب (webapps.config)

تفعيل/إلغاء تفعيل لكل تطبيق ويب مثبت.

الخصائص هي كما يلي:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

يتم تكوينه عبر /configadvanced في وحدة تحكم الـ router.

## التطبيقات

### دفتر العناوين (addressbook/config.txt)

راجع الوثائق في SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

يتم تكوينه عبر واجهة التطبيق الرسومية.

### i2psnark فردي (i2psnark.config.d/*/*.config)

إعداد torrent فردي. يتم تكوينه عبر واجهة المستخدم الرسومية للتطبيق.

### I2PTunnel (i2ptunnel.config)

يتم التكوين عبر تطبيق /i2ptunnel في وحدة تحكم router. اعتباراً من الإصدار 0.9.42، يتم تقسيم ملف i2ptunnel.config الافتراضي إلى ملفات تكوين فردية لكل tunnel في دليل i2ptunnel.config.d. بعد التقسيم، الخصائص في الملفات الفردية لا يتم إضافة بادئة "tunnel.N." لها.

ملاحظة: خيارات "tunnel.N.option.i2cp.*"، رغم أنها تبدو كخيارات I2CP، مُنفذة في i2ptunnel، وهي غير مدعومة عبر واجهات أو APIs أخرى مثل I2CP أو SAM.

الخصائص كالتالي:

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
ملاحظة: كل 'N' هو رقم tunnel يبدأ من 0. قد لا تكون هناك فجوات في الترقيم.

### وحدة تحكم Router

تستخدم وحدة تحكم الـ router ملف router.config.

### SusiMail (susimail.config)

راجع المنشور على zzz.i2p.

## المراجع

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [التطابق](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
