---
title: "Đặc Tả Tệp Cấu Hình"
description: "Đặc tả các tệp cấu hình I2P được sử dụng bởi router và các ứng dụng"
slug: "configuration"
aliases:
  - "/vi/configuration"
  - "/vi/configuration/"
category: "Định dạng"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Tổng quan

Trang này cung cấp đặc tả tổng quát về các tệp cấu hình I2P, được sử dụng bởi router và các ứng dụng khác nhau. Nó cũng đưa ra tổng quan về thông tin chứa trong các tệp khác nhau, và liên kết đến tài liệu chi tiết khi có sẵn.

## Định dạng chung

Một tệp cấu hình I2P được định dạng theo đặc tả trong Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) với các ngoại lệ sau:

- Mã hóa phải là UTF-8
- Không sử dụng hoặc nhận biết bất kỳ ký tự thoát nào, bao gồm `\`, do đó các dòng không thể được tiếp tục
- `#` hoặc `;` bắt đầu một bình luận, nhưng `!` thì không
- `#` bắt đầu bình luận ở bất kỳ vị trí nào nhưng `;` phải ở cột 1 để bắt đầu bình luận
- Khoảng trắng ở đầu và cuối không được loại bỏ trên các key
- Khoảng trắng ở đầu và cuối được loại bỏ trên các value
- `=` là ký tự kết thúc key duy nhất (không phải `:` hoặc khoảng trắng)
- Các dòng không có `=` sẽ bị bỏ qua. Kể từ bản phát hành 0.9.10, các key có giá trị "" được hỗ trợ.
- Vì không có ký tự thoát, các key không được chứa `#`, `=`, hoặc `\n`, hoặc bắt đầu bằng `;`
- Vì không có ký tự thoát, các value không được chứa `#` hoặc `\n`, hoặc bắt đầu hoặc kết thúc bằng `\r` hoặc khoảng trắng

Tệp không cần thiết phải được sắp xếp, nhưng hầu hết các ứng dụng sẽ sắp xếp theo khóa khi ghi vào tệp, để dễ đọc và chỉnh sửa thủ công.

Các thao tác đọc và ghi được triển khai trong DataHelper loadProps() và storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html). Lưu ý rằng định dạng tệp khác biệt đáng kể so với định dạng được tuần tự hóa cho các giao thức I2P được chỉ định trong [Mapping](/docs/specs/common-structures/#type-mapping).

## Thư viện lõi và router

### Clients (clients.config)

Được cấu hình thông qua /configclients trong bảng điều khiển router. Kể từ phiên bản 0.9.42, tệp clients.config mặc định được chia thành các tệp cấu hình riêng biệt cho từng client trong thư mục clients.config.d. Sau khi được chia, các thuộc tính trong các tệp riêng lẻ sẽ có tiền tố "clientApp.0.".

Định dạng như sau:

Các dòng có dạng `clientApp.x.prop=val`, trong đó x là số thứ tự ứng dụng. Số thứ tự ứng dụng PHẢI bắt đầu từ 0 và liên tiếp.

Các thuộc tính như sau:

**main** : Tên class đầy đủ. Bắt buộc. : Constructor hoặc phương thức main() trong class này sẽ được chạy, tùy thuộc vào việc client được quản lý hay không được quản lý. Xem chi tiết bên dưới.

**name** : Tên sẽ được hiển thị trên console.

**args** : Các đối số cho lớp chính, được phân tách bằng dấu cách hoặc tab. Các đối số chứa dấu cách hoặc tab có thể được đặt trong dấu ngoặc kép `'` hoặc `"`

**delay** : Số giây trước khi bắt đầu, mặc định 120

**onBoot** : `{true|false}` : Mặc định false, buộc độ trễ bằng 0, ghi đè cài đặt độ trễ

**startOnLoad** : `{true|false}` : Client có được chạy hay không? Mặc định true

Các thuộc tính bổ sung sau đây chỉ được sử dụng bởi các plugin:

**stopargs** : Các tham số để dừng client.

**uninstallargs** : Các tham số để gỡ cài đặt client.

**classpath** : Các phần tử classpath bổ sung cho client, phân tách bằng dấu phẩy.

Các thay thế sau được thực hiện trong các dòng args, stopargs, uninstallargs, và classpath, chỉ dành cho plugins:

**$I2P** : Thư mục cài đặt I2P cơ sở

**$CONFIG** : Thư mục cấu hình của người dùng (ví dụ: ~/.i2p)

**$PLUGIN** : Thư mục của plugin này (ví dụ: ~/.i2p/plugins/foo)

**$OS** : Tên hệ điều hành (ví dụ: "linux")

**$ARCH** : Tên kiến trúc (ví dụ: "amd64")

Tất cả các thuộc tính ngoại trừ "main" đều là tùy chọn. Các dòng bắt đầu bằng `#` là chú thích.

Nếu độ trễ nhỏ hơn không, client sẽ đợi cho đến khi router đạt trạng thái RUNNING và sau đó khởi động ngay lập tức trong một thread mới.

Nếu độ trễ bằng không, client sẽ được chạy ngay lập tức, trong cùng một thread, để các exception có thể được truyền lên console. Trong trường hợp này, client nên ném ra một exception, return nhanh chóng, hoặc tạo ra thread riêng của nó.

Nếu độ trễ lớn hơn không, nó sẽ được chạy trong một luồng mới và các ngoại lệ sẽ được ghi lại nhưng không được truyền đến console.

Client có thể được "quản lý" hoặc "không được quản lý".

### Logger (logger.config)

Được cấu hình thông qua /configlogging trong bảng điều khiển router.

Các thuộc tính như sau:

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
### Plugin Riêng Lẻ (plugins/*/plugin.config)

Xem [đặc tả plugin](/docs/specs/plugin). Lưu ý rằng các plugin cũng có thể chứa các tệp clients.config, i2ptunnel.config, và webapps.config.

### Plugins (plugins.config)

Bật/tắt cho từng plugin đã cài đặt.

Các thuộc tính như sau:

```
plugin.{name}.startOnLoad=true|false
```
### Ứng dụng web (webapps.config)

Bật/tắt cho từng webapp đã cài đặt.

Các thuộc tính như sau:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Được cấu hình thông qua /configadvanced trong bảng điều khiển router.

## Ứng dụng

### Sổ địa chỉ (addressbook/config.txt)

Xem tài liệu trong SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Được cấu hình thông qua giao diện người dùng của ứng dụng.

### i2psnark cá nhân (i2psnark.config.d/*/*.config)

Cấu hình cho một torrent riêng lẻ. Được cấu hình thông qua giao diện người dùng của ứng dụng.

### I2PTunnel (i2ptunnel.config)

Được cấu hình thông qua ứng dụng /i2ptunnel trong bảng điều khiển router. Kể từ phiên bản 0.9.42, tệp i2ptunnel.config mặc định được tách thành các tệp cấu hình riêng lẻ cho từng tunnel trong thư mục i2ptunnel.config.d. Sau khi được tách, các thuộc tính trong các tệp riêng lẻ KHÔNG được đặt tiền tố "tunnel.N.".

Lưu ý: Các tùy chọn "tunnel.N.option.i2cp.*", mặc dù có vẻ như là các tùy chọn I2CP, nhưng được triển khai trong i2ptunnel và KHÔNG được hỗ trợ thông qua các giao diện hoặc API khác như I2CP hoặc SAM.

Các thuộc tính như sau:

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
Lưu ý: Mỗi 'N' là một số tunnel bắt đầu từ 0. Không được có khoảng trống trong việc đánh số.

### Router Console

Router console sử dụng tệp router.config.

### SusiMail (susimail.config)

Xem bài viết trên zzz.i2p.

## Tài liệu tham khảo

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Ánh xạ](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
