---
title: "BOB - Basic Open Bridge"
description: "Deprecated API for destination management"
slug: "bob"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Warning - Deprecated

Not for use by new applications. BOB, as specified here, supports the DSA-SHA1 signature type only. BOB will not be extended to support new signature types or other advanced features. New applications should use [SAM V3](/docs/api/samv3).

BOB support was removed from Java I2P new installs as of release 1.7.0 (2022-02). It will still work in Java I2P originally installed as version 1.6.1 or earlier, even after updates, but it is unsupported and may break at any time. BOB is still supported by i2pd as of 2025-05, but applications should still migrate to SAMv3 for the reasons above. See [the i2pd documentation](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) for any extensions to the API documented here that are supported by i2pd.

At this point, most of the good ideas from BOB have been incorporated into SAMv3, which has more features and more real-world use. BOB may still work on some installations (see above), but it is not gaining the advanced features available to SAMv3 and is essentially unsupported, except by i2pd.

## Language Libraries for the BOB API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Overview

`KEYS` = keypair public+private, these are BASE64

`KEY` = public key, also BASE64

`ERROR` as is implied returns the message `"ERROR "+DESCRIPTION+"\n"`, where the `DESCRIPTION` is what went wrong.

`OK` returns `"OK"`, and if data is to be returned, it is on the same line. `OK` means the command is finished.

`DATA` lines contain information that you requested. There may be multiple `DATA` lines per request.

**NOTE:** The help command is the ONLY command that has an exception to the rules... it can actually return nothing! This is intentional, since help is a HUMAN and not an APPLICATION command.

## Connection and Version

All BOB status output is by lines. Lines may be \\n or \\r\\n terminated, depending on the system. On connection, BOB outputs two lines:

```
BOB version
OK
```

The current version is: 00.00.10

Note that previous versions used upper-case hex digits and did not conform to I2P versioning standards. It is recommended that subsequent versions use digits 0-9 only.

### Version History

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>

## Commands

**PLEASE NOTE:** For CURRENT details on the commands PLEASE use the built-in help command. Just telnet to localhost 2827 and type help and you can get full documentation on each command.

Commands never get obsoleted or changed, however new commands do get added from time to time.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```

Once set up, all TCP sockets can and will block as needed, and there is no need for any additional messages to/from the command channel. This allows the router to pace the stream without exploding with OOM like SAM does as it chokes on attempting to shove many streams in or out one socket -- that can't scale when you have a lot of connections!

What is also nice about this particular interface is that writing anything to interface to it, is much much easier than SAM. There is no other processing to do after the set up. Its configuration is so simple, that very simple tools, such as nc (netcat) can be used to point to some application. The value there is that one could schedule up and down times for an application, and not have to change the application to do that, or to even have to stop that application. Instead, you can literally "unplug" the destination, and "plug it in" again. As long as the same IP/port addresses and destination keys are used when bringing the bridge up, the normal TCP application won't care, and won't notice. It will simply be fooled -- the destinations are not reachable, and that nothing is coming in.

## Examples

For the following example, we'll setup a very simple local loopback connection, with two destinations. Destination "mouth" will be the CHARGEN service from the INET superserver daemon. Destination "ear" will be a local port that you can telnet into, and watch the pretty ASCII test puke forth.

### Example Session Dialogue

Simple telnet 127.0.0.1 2827 works.

- A = Application
- C = BOB's Command response.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```

**MAKE NOTE OF THE ABOVE DESTINATION KEY, YOURS WILL BE DIFFERENT!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```

At this point, there was no error, a destination with a nickname of "mouth" is set up. When you contact the destination provided, you actually connect to the `CHARGEN` service on `19/TCP`.

Now for the other half, so that we can actually contact this destination.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```

Now all we need to do is telnet into 127.0.0.1, port 37337, send the destination key or host address from address book we want to contact. In this case, we want to contact "mouth", all we do is paste in the key and it goes.

**NOTE:** The "quit" command in the command channel does NOT disconnect the tunnels like SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```

After a few virtual miles of this spew, press `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```

Here is what happened...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```

You can connect to I2P SITES too!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```

Pretty cool isn't it? Try some other well known I2P SITES if you like, nonexistent ones, etc, to get a feel for what kind of output to expect in different situations. For the most part, it is suggested that you ignore any of the error messages. They would be meaningless to the application, and are only presented for human debugging.

### Cleaning Up

Let's put down our destinations now that we are all done with them.

First, lets see what destination nicknames we have.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```

Alright, there they are. First, let's remove "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```

Now to remove "ear", note that this is what happens when you type too fast, and shows you what typical ERROR messages looks like.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```

## Quiet Mode

I won't bother to show an example of the receiver end of a bridge because it is very simple. There are two possible settings for it, and it is toggled with the "quiet" command.

The default is NOT quiet, and the first data to come into your listening socket is the destination that is making the contact. It is a single line consisting of the BASE64 address followed by a newline. Everything after that is for the application to actually consume.

In quiet mode, think of it as a regular Internet connection. No extra data comes in at all. It's just as if you are plain connected to the regular Internet. This mode allows a form of transparency much like is available on the router console tunnel settings pages, so that you can use BOB to point a destination at a web server, for example, and you would not have to modify the web server at all.

## Advantages of BOB

The advantage with using BOB for this is as discussed previously. You could schedule random uptimes for the application, redirect to a different machine, etc. One use of this may be something like wanting to try to goof up router-to-destination upness guessing. You could stop and start the destination with a totally different process to make random up and down times on services. That way you would only be stopping the ability to contact such a service, and not have to bother shutting it down and restarting it. You could redirect and point to a different machine on your LAN while you do updates, or point to a set of backup machines depending on what is running, etc, etc. Only your imagination limits what you could do with BOB.
