---
title: "Reunión de desarrolladores de I2P"
date: 2003-07-15
author: "nop"
description: "Reunión de desarrollo de I2P que abarca actualizaciones del proyecto y discusiones técnicas"
categories: ["meeting"]
---

(Cortesía de la Wayback Machine http://www.archive.org/)

## Resumen rápido

<p class="attendees-inline"><strong>Presentes:</strong> gott, hezekiah, jeremiah, jrand0m, mihi, Neo, nop, WinBear</p>

## Registro de la reunión

<div class="irc-log"> --- Log opened Tue Jul 15 17:46:47 2003 17:46 < gott> yo. 17:46 <@nop> just a heads up on my silence 17:46 <@hezekiah> Tue Jul 15 21:46:49 UTC 2003 17:47 <@hezekiah> OK. The iip-dev meeting has started. 17:47 <@hezekiah> Is it the 48th or 49th? 17:47 < jrand0m> nop> this is why its critical that we get the router 	architecture pounded out asap.  I understand that different people have 	different rates of speed, and we must segment so different components can 	proceed accordingly 17:47 < mihi> 49th 17:47 <@hezekiah> OK! Welcome to the 49th iip-dev meeting! 17:47 < jrand0m> I have three more days at my job, after which 90+ hours / 	week will be dedicated to getting this going 17:48 < jrand0m> I know and don't expect everyone to be able to do that, 	which is why we need to segment 17:48 < jrand0m> hi hezekiah :) 17:48 <@hezekiah> lol 17:48 <@nop> to rebutt on that 17:48 <@hezekiah> I'll wait a minute. Then we can do the agenda. :) 17:48 <@nop> the security of the router architecture is dependant that you 	do not rush as well 17:49 <@nop> if we do 17:49 <@nop> we overlook 17:49 <@nop> which could leave us cleaning up a big mess later 17:49 -!- Rain [Rain@anon.iip] has quit [I Quit] 17:49 < jrand0m> nop> disagree.  we can still build app layer and APIs 	without implementing the router (or even knowing how the network will operate) 17:49 <@nop> I agree with that 17:50 <@nop> I'm specifically talking about the underlying network 17:50 < jrand0m> if we can agree to the API I sent out, then thats the 	segmentation we need 17:50 < jrand0m> right, router impl and network design still isn't done 17:50 <@nop> ok 17:50 <@nop> oh, I can definitely agree with your api so far 17:51 <@hezekiah> jrand0m: One problem. 17:51 < jrand0m> shoot hezekiah 17:51 <@hezekiah> It will look different if you implement it in C. 17:51 < jrand0m> not too different 17:51 < gott> oh dear 17:51 < jrand0m> less capital letters, and replace the objects with structs 17:51 < gott> what languages are people considering implementing it in? 17:51 < jrand0m> (for the api) 17:51 <@hezekiah> Uh, jrand0m? There is no 'byte[]' in C. 17:51 < jrand0m> gott> read the mail archives for some example answers to that 17:52 <@hezekiah> You will be using void*'s with an integer to specifiy the 	length most likely. 17:52 < jrand0m> hezekiah> then unsigned int[] 17:52 < gott> jrand0m: for once, a religious war that I'm not a part of 17:52 <@hezekiah> If I remember correctly (help me out here nop), you can't 	just return an unsigned int[] from a function. 17:53 <@hezekiah> gott: as opposed to what? pseudocode? 17:53 < jrand0m> right, syntactic changes.  but yes, if there are real 	differences, we need to get them worked out ASAP.  (like, today)  Perhaps 	now would be a good tiem to look at the email I sent entitled "high level 	router architecture and API" and review? 17:54 <@hezekiah> nop? UserX? Are you game for that? 17:54 < jrand0m> not too different, but different none the less, yes. 	which is why I said Java API on todays email :) 17:54 -!- WinBear [WinBear@anon.iip] has joined #iip-dev 17:55 <@nop> wait 17:55 <@nop> reading above 17:55 -!- mihi_2 [~none@anon.iip] has joined #iip-dev 17:55 -!- mihi is now known as nickthief60234 17:55 -!- mihi_2 is now known as mihi 17:55 < jrand0m> wb mihi 17:55 < gott> btw, is this being live logged? 17:55 -!- nickthief60234 [~none@anon.iip] has quit [EOF From client] 17:55 <@hezekiah> gott: Yes. 17:55 < mihi> redundancy rules ;) 17:55 < gott> I'll just read it later on then. 17:55 -!- gott [~gott@anon.iip] has left #iip-dev [gott] 17:56 <@nop> ok 17:56 <@nop> yes 17:56 < WinBear> jrand0m: hi 17:56 <@nop> definitely differences 17:56 <@nop> what we need 17:56 < jrand0m> heya WinBear 17:56 <@nop> is a team of certain developers to write the main api level 	controls for these languages 17:56 <@nop> we know that jrand0m can handle java 17:56 <@nop> and probably could team up with thecrypto as well 17:56 <@nop> and hezekiah and the gang can do C 17:56 <@nop> and jeremiah if he's willing 17:56 <@nop> can do python 17:56 <@hezekiah> I can do C++ too! ;-) 17:56 <@nop> ok 17:56 <@nop> C++ as well 17:57 <@hezekiah> lol 17:57 <@nop> C++ will probably work 17:57 <@nop> with C 17:57 <@nop> if you don't template the crap out of it 17:57 < jrand0m> heh 17:57 <@hezekiah> lol 17:57 <@hezekiah> Actually, while MSVC can link C and C++ object files, 	gcc doesn't seem to like that. 17:57 <@nop> aka, stick to structs that are compatible with C, or is that 	not viable 17:57 < jrand0m> first question, prior to that, is what applications will use 	these APIs?  I know of apps that will want to use java, will iproxy be in C? 17:58 <@hezekiah> nop: I don't think C and C++ are object compatible. 17:58 <@nop> ok 17:58 <@hezekiah> nop: C++ won't get along with C much better than Java. 17:58 <@nop> well maybe USerX could do C 17:58 <@nop> and you could pull C++ 17:58 <@hezekiah> We don 17:58 <@nop> ? 17:58 <@hezekiah> don't even need to _do_ C++ if you don't want to. It's 	just that I prefer it. 17:59 <@nop> well, the thing is 17:59 <@nop> there are a lot of C++ developers 17:59 <@nop> especially in the microsoft world 17:59 <@hezekiah> Even in the Linux world. (see: KDE and Qt.) 17:59 < jrand0m> C and C++ are binary compatible if you just make .so or .a 17:59 < jrand0m> (btw) 18:00 <@nop> can C be a good placement for C++, aka C++ developers would be 	able to handle a c api easier than a C++ api with a c developer? 18:00 <@hezekiah> jrand0m: Yeah. You can probably have libraries ... but if 	you can 18:00 <@hezekiah> jrand0m: can't even use classes, it sorta defeats the 	purpose. 18:00 <@nop> right 18:00 <@nop> let's stick with C 18:01 <@nop> because C++ coders can still call a C library rather easily 18:01 <@hezekiah> If one module needs to call anothers functions, then they 	had best both be the same language. 18:01 <@hezekiah> nop: C++ coders will know C well enough ... though it 	might take some work if they never /learned/ C. 18:02 <@hezekiah> However, C coders wouldn't know C++ since C is just a 	subset of C++. 18:02 -!- logger_ [~logger@anon.iip] has joined #iip-dev 18:02 -!- Topic for #iip-dev: logfiles will be online after the meeting: 	http://wiki.invisiblenet.net/?Meetings 18:02 [Users #iip-dev] 18:02 [@hezekiah] [+Ehud    ] [ leenookx] [ moltar] [ tek    ] 18:02 [@nop     ] [ jeremiah] [ logger_ ] [ Neo   ] [ WinBear] 18:02 [@UserX   ] [ jrand0m ] [ mihi    ] [ ptsc  ] 18:02 -!- Irssi: #iip-dev: Total of 14 nicks [3 ops, 0 halfops, 1 voices, 10 normal] 18:02 < jrand0m> right 18:02 -!- Irssi: Join to #iip-dev was synced in 9 secs 18:02 < jrand0m> (with JMS :) 18:02 <@nop> yep 18:03 -!- You're now known as logger 18:03 < jrand0m> ok, can we review the overall architecture to see whether 	the APIs are even relevent first? 18:03 <@nop> fine  18:04 < jrand0m> :) 18:04 < jrand0m> ok, see the email I sent w/ the routerArchitecture.png. 	any thoughts on that seperation? 18:04 -!- tek [~tek@anon.iip] has quit [] 18:05 < WinBear> jrand0m: is that on the wiki? 18:05 < jrand0m> WinBear> no, on the mailing list, though the archives 	are down.  lemmie add it to the wikki 18:06 <@hezekiah> Correct me if I'm wrong ... 18:07 <@hezekiah> ... but it looks like we're going to have 3 seperate API's 	that are as similar as possible. 18:07 <@hezekiah> Right? 18:07 < jrand0m> yes hezekiah 18:07 <@hezekiah> So since each API is in a different language, are they 	going all each have seperate implementations? 18:07 < jrand0m> yes 18:07 <@hezekiah> Or is there a way for Java or Python to access a C library? 18:08 < jrand0m> yes, but we don't want to go that route 18:08 < mihi> for java: JNI 18:08 <@hezekiah> So this talk about Java, C, C++, Python, etc. working 	together is mute since they never will? 18:08 < jrand0m> how do I attach an image to the wiki? 18:08 <@hezekiah> Each API has its own backend written in that language. 18:08 < jrand0m> no hezekiah, look at the diagram 18:09 <@hezekiah> Oh, duh! 18:09 <@hezekiah> The API's don't link to a backend. 18:10 <@hezekiah> They talk via sockets. 18:10 < jrand0m> si sr 18:10 <@hezekiah> This is still a little confusing though. 18:10 <@hezekiah> Give me a sec here. :) 18:11 <@hezekiah> OK. What is the thing labeled 'transport'? 18:11 < jrand0m> for example, bidirectional HTTP transport, SMTP transport, 	plain socket transport, polling HTTP socket, etc 18:11 < jrand0m> the thing that moves bytes between routers 18:12 <@hezekiah> OK. 18:12 <@hezekiah> So the diagram I'm looking at shows one person's computer. 18:12 <@hezekiah> He has a router that talks to other people's computers 	via the transports. 18:12 < jrand0m> correct 18:12 <@hezekiah> Person 1 (Alice) has 2 applications running. 18:12 <@hezekiah> One is in C, the other in Java. 18:13 <@hezekiah> Both are linked to a library (that's the API). 18:13 < jrand0m> both are "linked" to seperate libraries (the APIs) 18:13 <@nop> simple concept 18:13 <@nop> yes 18:13 <@hezekiah> Those libraries, take input from the program encrypt it, 	and send it via sockets (unix or TCP) to the router ... which is another 	program Alice is running. 18:13 < jrand0m> correct 18:14 <@hezekiah> OK. So it's kinda like isproxy being split in two. 18:14 < jrand0m> bingo :) 18:14 <@hezekiah> One part is low end and written in C, and the other is 	high end and written in whatever. 18:14 < jrand0m> exactly 18:14 <@hezekiah> OK. I get it. :) 18:14 < jrand0m> w00t 18:14 <@hezekiah> So no language needs to play nice with any other language. 18:14 < jrand0m> WinBear> sorry, I can't toss it on the wiki as it only 	takes text :/ 18:15 <@hezekiah> Since they all comunicate with the router via sockets, 	you could write an API in PASCAL for all the design cares. 18:15 <@nop> yes 18:15 <@nop> arbitrary 18:15 < jrand0m> right 18:15 <@nop> it handles arbitrary sockets 18:15 < jrand0m> though some things need to be standardized (like the data 	structures for Destination, Lease, etc) 18:15 < WinBear> jrand0m: i get a vague idea based on what hezekiah is saying 18:15 < jrand0m> word 18:16 <@hezekiah> jrand0m: Right. The structure and order of the bytes that 	go across that socket is set in a design somewhre 18:16 <@hezekiah> somewhere. 18:17 <@hezekiah> But you can still implement how those bytes are send and 	received any joly way you please. 18:17 <@nop> WinBear: it's the same exact way that the irc client works 	with isproxy 18:17 < jrand0m> exactly 18:17 <@hezekiah> Good. 18:17 <@hezekiah> I understand now. :) 18:17 -!- moltar [~me@anon.iip] has left #iip-dev [moltar] 18:17 <@nop> well 18:17 <@nop> not exactly 18:17 <@hezekiah> Uh oh. 18:17 <@nop> but imagine how that works 18:17 <@nop> and you can understand arbitrary sockets 18:17 <@nop> isproxy just routes 18:17 <@nop> and delivers 18:18 <@nop> now jrand0m 18:18 <@nop> quick question 18:18 < jrand0m> si sr? 18:18 <@nop> is this api designed for only new applications that are designed 	to work on this network 18:18 -!- mode/#iip-dev [+v logger] by hezekiah 18:18 < WinBear> nop: with the highlevel replacing the irc client? 18:18 < jrand0m> nop> yes.  though a SOCKS5 proxy could use this API as well 18:18 <@nop> or can it be able to have a middle man that can allow already 	standard clients 18:18 <@nop> for instance 18:19 <@nop> so all we would have to do is write the middleman -> api 18:19 < jrand0m> (but note that there's no 'lookup' service available - 	no DNS for this network) 18:19 < jrand0m> correct 18:19 <@nop> so that we can support say Mozilla etc 18:19 <@nop> so they can just code plugins 18:19 < jrand0m> nop> yes 18:19 <@nop> ok 18:19 <@nop> or transports :) 18:20 < jrand0m> (e.g. the SOCKS5 has the HTTP outproxies hardcoded to 	destination1, destination2, and destination3) 18:20 <@nop> ok 18:20 < WinBear> i think i get it 18:21 < jrand0m> w00t 18:21 < jrand0m> ok, one of the things I had to think about in this design 	was keeping the private keys in the app's memory space - the router never 	gets a hold of destination private keys. 18:21 <@hezekiah> So the application can send raw data over the I2P network 	by sending it to the API, and it doesn't need to worry about the rest. 18:22 <@hezekiah> Right? 18:22 < jrand0m> that means the APIs need to implement the end to end part 	of the crypto 18:22 < jrand0m> exactly hezekiah 18:22 <@hezekiah> OK. 18:22 <@nop> yes 18:22 <@nop> that's the idea 18:22 <@nop> it does it for you 18:22 <@nop> you just call the hook 18:23 <@hezekiah> One quick question: 18:23 <@hezekiah> This 'router' obviously needs to speak a certain protocol 	over it's transports. 18:23 < jrand0m> correct 18:23 <@hezekiah> So it is possible to provide multiple implementations of 	the router ... 18:23 < jrand0m> yes 18:24 <@hezekiah> ... as long as they both speak the same protocol. 18:24 < jrand0m> (which is why the spec has placeholders for bitbuckets) 18:24 < jrand0m> right 18:24 <@hezekiah> So you have a router in Java, and one in C, and one 	in PASCAL. 18:24  * jrand0m cringes 18:24 < jrand0m> but yeah 18:24 <@hezekiah> And they all can talk together since they're talking over 	TCP/IP using the same protocol. 18:24  * WinBear jumps 18:24 <@hezekiah> jrand0m: And yes. I don't remember my PASCAL days overly 	fondly either. 18:25 < jrand0m> well, Pascal can talk to the C one through the TCP transport, 	and the C one can talk to the Java one over the HTTP transport, for example 18:25 <@hezekiah> Right. 18:25 < jrand0m> (transports talk to other like transports, routers manage 	the messages delivered between them but don't deal with how they're delivered) 18:26 <@hezekiah> The point I was looking to make was that the protocol is the 	same, so it doesn't matter what language someone's router is implemented in. 18:26 < jrand0m> right 18:26 <@hezekiah> Cool. 18:26 < jrand0m> now you understand why I said "who cares" to all the C vs 	Java vs etc debates?  :) 18:26 <@hezekiah> Yup. 18:26 <@hezekiah> lol 18:27 <@hezekiah> I've got to hand it to you jrand0m. This will make it very 	kind for develoeprs to write programs for this network. 18:27 < jrand0m> heh, well, the API ain't quite original.  this is how 	Message Oriented Middleware (MOM) works 18:27 <@hezekiah> And you could even make routers that specialize in certain 	platform specific features (like 64-bit CPU's). 18:28 < jrand0m> absolutely 18:28 <@hezekiah> jrand0m: Humble too! ;-) 18:28 <@hezekiah> Well, it looks good to me. 18:28 < jrand0m> ok, UserX, nop, does this seperation make sense? 18:28 <@nop> of course 18:28 <@nop> is userx still here 18:29 <@hezekiah> He's been idle for 1:26. 18:29 < jrand0m> 'k.  so then we have two tasks: design the network, and 	design how the API works. 18:29 <@nop> right 18:29 <@hezekiah> Quick simple question: The API's do end to end crypto. Do 	the routers to node to node crypto ? 18:29 <@nop> yes 18:30 < jrand0m> yes 18:30 < jrand0m> (transport level) 18:30 <@hezekiah> Good. :) 18:30 <@nop> hezekiah: it's very similar to what we have so far 18:30 <@nop> in that aspect 18:31 < jrand0m> ok.. er, shit, thecrypto aint around for comments on the 	performance model. 18:31 < Neo> and for the paranoid, the apps can do the pgp encryption before 	it hits the API ;) 18:31 < jrand0m> absolutely neo 18:31 < jrand0m> I was even tempted to leave the end to end crypto out of 	the API and leave it up to the apps... 18:31 <@hezekiah> jrand0m: That would be cruel. 18:31 < jrand0m> heheh 18:32 <@hezekiah> BTW, the API's and the router communicate via sockets. 18:32 <@hezekiah> On UNIX will they be using UNIX sockets or local TCP/IP 	sockets? 18:32 < jrand0m> prolly just local tcp/ip for simplicity 18:32 <@nop> hold 18:32 <@hezekiah> (I suppose you could make a router that accepts both.) 18:33  * hezekiah is really liking this interchangable parts setup 18:33 <@nop> if you hold on a sec 18:34 <@hezekiah> Holding ... :) 18:34 <@nop> I'll call thecrypto at his house 18:34 <@nop> see if he can get on 18:34 < jrand0m> hehe word 18:34 <@hezekiah> lol 18:34  * hezekiah dons a thick Itallian accent 18:34 <@hezekiah> Nop ha' got ... CONNECTIONS! 18:34 < jeremiah> lo 18:34 <@nop> hey jeremiah 18:35 < jrand0m> heya jeremiah 18:35 <@nop> would you be willing at the api level to assist with a python api 18:35 < jeremiah> sure 18:35  * jeremiah reads backlog 18:35 < jrand0m> heh word 18:35  * nop is calling 18:36 <@nop> he's not home 18:36 <@nop> he'll be back in an hour 18:36 < jrand0m> 'k, has anyone else read the .xls and/or have comments on 	the model? 18:37 <@hezekiah> I read the .xls ... but I don't know much about p2p so 	most of it was over my head. 18:37 <@hezekiah> UserX is good at that stuff. 18:37 <@nop> I have to read it still 18:37 < jrand0m> (btw, morphmix had some insane numbers... they were saying 	they could expect random hosts on the net to have average 20-150ms ping times, 	rather than the 3-500 I was expecting) 18:37 < jrand0m> coo' 18:37 <@nop> it's staroffice or openoffice? 18:37 < jrand0m> openoffice, but I exported it to .xls 18:37 <@nop> which is excell? 18:37 < jrand0m> correct 18:38 <@hezekiah> BTW, concerning the API ... 18:38 < jrand0m> si sr? 18:38 <@hezekiah> ... in C the boolean would be int. 18:38 <@nop> which email 18:38 <@nop> hezekiah: yes 18:38 <@hezekiah> The classes would be sent as structure pointers. 18:38 <@nop> unless you typedef boolean 18:39 <@hezekiah> And the functions that use byte[] would use a void* with 	an additional parameter that specefies the length of the buffer. 18:39 <@nop> hezekiah: you're being picky :) 18:39 < jrand0m> nop> I cant access the archives so I'm not sure what the 	subject line was, but it was last week... 18:39 <@nop> save it for a later time 18:39 <@hezekiah> nop: Picky? 18:39 < jrand0m> heh, yeah, y'all working on the C api can work that detail out 18:39  * jeremiah is done reading backlog 18:39 <@nop> what's the file called 18:39 <@hezekiah> nop: I'm just trying to find all the stuff that is different, 	so we can hammer it out like jrand0m asked. 18:40 <@hezekiah> I'm trying to be helpful. :) 18:40 <@nop> hezekiah: yes, probably off meeting time 18:40 < jrand0m> nop> simple_latency.xls 18:40 <@hezekiah> boolean sendMessage(Destination dest, byte[] payload); 18:40 <@hezekiah>  would be 18:40 <@hezekiah> int sendMessage(Destination dest, void* payload, int length); 18:40 <@hezekiah> . 18:40 <@hezekiah> byte[]  recieveMessage(int msgId); 18:40 <@hezekiah>  that could either be: 18:41 <@hezekiah> void*  recieveMessage(int msgId, int* length); 18:41 <@hezekiah>  or 18:41 <@nop> jrand0m: got it 18:41 <@hezekiah> void recieveMessage(int msgId, void* buf, int* length); 18:41 <@hezekiah>  or 18:41 < jrand0m> hezekia: why not typedef struct { int length; void* data; 	} Payload; 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId)l 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId); 18:41 < jeremiah> where's this xls? 18:41 <@nop> oh iip-dev 18:41 <@hezekiah> jrand0m: The struct you just mentioned is basically what 	DataBlock is. 18:42 < jrand0m> word hezekiah 18:42 <@nop> subject more models 18:42 <@hezekiah> Chances are the C version would have DataBlocks. 18:43 <@hezekiah> Beyond that the only other thing to note is that each 	'interface' would just be a set of functions. 18:43 <@hezekiah> nop: Did I find all the differences that would exist in 	a C API? 18:43 < jrand0m> right.  perhaps #include "i2psession.h" or something 18:43 < jeremiah> is there a mockup python api? 18:44 < jrand0m> no jeremiah, I don't really know python :/ 18:44 <@nop> I would have to re-review the java api, but I would say that 	you're right on target 18:44 < jrand0m> but it would probably be similar to the java, as python is OO 18:44 < jeremiah> cool, i can derive one from the C one 18:44  * nop is not a java head 18:44 < jrand0m> cool jeremiah 18:44 < jeremiah> is the c api in the thing you sent out a few days ago? 18:44 <@hezekiah> Yeah. Python should be able to handle the Java api. 18:44 < jrand0m> jeremiah> that was the Java one 18:45 < jrand0m> oh, the Java one was today 18:45 < jrand0m> the older one was language independent 18:45 <@hezekiah> Hmm 18:45 <@nop> UserX says he should be able to assist with C api 18:45 < jrand0m> word 18:45 <@nop> he's busy at work at the moment 18:46 < jrand0m> coo' 18:46 <@hezekiah> One last note: With the C api, each function would probably 	take a structure* to the structure that it is an 'interface' of in Java. 18:46 <@nop> hezekiah: loos good 18:46 <@nop> looks good 18:46 <@hezekiah> I2PSession       createSession(String keyFileToLoadFrom, 	Properties options); 18:46 <@hezekiah>  would be: 18:46 <@nop> java and their non-native data types 18:46 <@hezekiah> I2PSession* createSession(I2PClient* client, char* 	keyFileToLoadFrom, Properties* options); 18:46 <@nop> ;) 18:46 < jrand0m> hehe 18:46 < jrand0m> right hezekiah 18:47 < jeremiah> are we addressing unicode? 18:47 <@hezekiah> Anyway, if you can live with those differences, the C and 	Java API's should be identical beyond that. 18:47 <@hezekiah> nop? Unicode? :) 18:47 < jrand0m> UTF8 if not UTF16 18:48 <@hezekiah> Perhaps Unicode should be dealt with on the application 	level. 18:48 < jrand0m> right, charset is all the content of the message 18:48 <@hezekiah> Oh. 18:48 < jeremiah> ok 18:48 <@hezekiah> Java String's are done in Unicode, aren't they jrand0m? 18:48 < jrand0m> the bitbuckets'll all be bit defined 18:48 < jrand0m> yes hezekiah 18:48 < jrand0m> (unless you explicitly instruct them to change charsets) 18:49 <@hezekiah> So the string sent to the Java API would be different than 	the one sent to the C API unless the C API implements strings using Unicode. 18:49 < jrand0m> not relevent 18:49 <@hezekiah> OK. 18:49 < jrand0m> (app->API != API->router.  we only define API->router) 18:49 <@hezekiah> What I'm saying is this, jrand0m: 18:50 <@hezekiah> If I set my password with the Java API, it goes to the 	router out someplace else. 18:50 < jrand0m> password?  you mean you create a Destination? 18:50 <@hezekiah> Then it find another router, which sends it to another API 	(?) which is implemented in C. 18:50 <@hezekiah>   void            setPassphrase(String old, String new); 18:50 <@hezekiah> That function. 18:51 < jrand0m> hezekiah> thats the administrative password to access the 	administrative methods of the router 18:51 <@hezekiah> Ah 18:51 <@hezekiah> Do any functions in the API which use Java String's end 	up with that String being sent to another API? 18:51 < jrand0m> 99.9% of apps will only use I2PSession, not I2PAdminSession 18:51 <@nop> also, anything carried with the router gets converted for 	network travel correct? 18:51 <@hezekiah> If so, we should probably use Unicode. 18:51 <@nop> unicode wouldn't be releavant 18:52 < jrand0m> hezekiah> no.  all inter-router info will be defined by 	bit buckets 18:52 <@hezekiah> OK. 18:52 < jrand0m> correct nop, at the transport level 18:52 <@hezekiah> (I'm assuming a bit bucket is just a binary buffer, right?) 18:53 < jrand0m> a bit bucket is a statement that the first bit means X, 	the second bit means Y, bits 3-42 mean Z, etc 18:53 < jrand0m> (e.g. we may want to use X.509 for the certificates bitbucket)

18:53 <@hezekiah> Nunca he lidiado con eso antes.
18:54 <@hezekiah> Me preocuparé por eso cuando llegue. :)
18:54 < jrand0m> je, cierto
18:55 < jrand0m> ok, las cuatro cosas que quería que abordáramos hoy: *arquitectura del router, *modelo de rendimiento, *análisis de ataques, *psyc.  Hemos hecho la primera, thecrypto está desconectado así que quizá lo retrasemos (a menos que tengas 	alguna idea sobre el modelo, nop?)
18:57 <@hezekiah> Eh... jrand0m. Tengo otra pregunta más.
18:57 < jeremiah> jrand0m: ¿dónde está la última versión de la especificación de la red? ¿es 	la que enviaste el día 13?
18:57 < jrand0m> si sr?
18:57 <@hezekiah> Bueno, la arquitectura del router hace que las API gestionen claves 	/enviadas por la aplicación/.
18:57 < jrand0m> jeremiah> sí
18:57 <@nop> No en este momento
18:58 <@hezekiah> Ahora... la única manera que veo de que la API obtenga la clave es 	desde createSession.
18:58 < jrand0m> hezekiah> el router 	obtiene claves públicas y firmas, 	no claves privadas
18:58 < jrand0m> correcto
18:58 <@hezekiah> Pero eso requiere un archivo.
18:58 < jrand0m> las claves se almacenan en un archivo o en la memoria de la API
18:58 < jrand0m> sí
18:58 <@hezekiah> Ahora, si la aplicación genera una clave, ¿por qué no puede simplemente 	enviarla a la API mediante un búfer?
18:59 <@hezekiah> ¿De verdad debe guardarla en un archivo y luego proporcionar el 	nombre del archivo?
18:59 < jrand0m> no, puede estar en memoria si quieres
18:59 <@hezekiah> Sin embargo, no hay una función para hacer todo eso en la API.
18:59 <@hezekiah> Es solo una idea.
19:00 <@hezekiah> Si se supone que la clave se genera una sola vez y se usa 	muchas, muchas veces (como las claves de GPG), entonces un archivo tiene sentido.
19:00 -!- mihi [none@anon.iip] ha salido [adiós a todos, se está haciendo tarde...]
19:00 <@hezekiah> Pero si se va a generar con más frecuencia, entonces quizá alguna 	manera de enviarla directamente a la API mediante una estructura o algún tipo de 	búfer podría estar bien
19:00 <@hezekiah> .
19:01 < jrand0m> sí, se genera una vez y solo una vez (a menos que lleves 	un sombrero de papel de aluminio)
19:02 < jrand0m> aunque createDestination(keyFileToSaveTo) te permite 	crear esa clave
19:02 <@hezekiah> OK.
19:02 <@hezekiah> Así que realmente no hay necesidad de transferir directamente de la 	aplicación a la API. Un archivo será suficiente.
19:03 <@hezekiah> Entonces, ¿en qué estábamos antes de que interrumpiera tan groseramente? :)
19:06 < jeremiah> entonces ahora mismo solo estamos trabajando en la API del router, no 	en la del cliente, ¿verdad?
19:06 < jrand0m> bueno, por ahora vamos a saltarnos el análisis de rendimiento 	(con suerte podemos conseguir algo de charla al respecto en la lista de correo antes de la 	próxima semana?).  y probablemente lo mismo con respecto al análisis de ataques (a menos que alguien haya leído la 	nueva especificación y tenga comentarios)
19:07 <@hezekiah> Entonces, ya que nos saltamos eso, ¿de qué se supone 	que debemos hablar ahora?
19:07 <@hezekiah> Psyc?
19:07 < jrand0m> a menos que alguien más tenga otros comentarios que plantear...?
19:08 <@hezekiah> Bueno, por una vez, mi agujero de comentarios (también notoriamente conocido 	como mi boca) está vacío.
19:08 < jrand0m> jeje
19:09 < jrand0m> bien, ¿alguien tiene alguna idea de cómo funcionará la parte de IRC y si psyc puede ser 	relevante o útil?
19:09 < jeremiah> nota aparte (que me molestó): la lista "Wired, Tired, 	Expired" de Wired tenía a Waste como 'wired'
19:09 < jrand0m> je
19:09 < jrand0m> ¿te das cuenta de cuánto vamos a dejar a todos boquiabiertos?
19:09 < jeremiah> sí
19:09 <@hezekiah> jrand0m: Eso supone que logremos que esto funcione.
19:10 < jrand0m> Garantizo que funcionará.
19:10 <@hezekiah> Hay muchos otros esfuerzos fallidos por ahí.
19:10 < jrand0m> Dejé mi trabajo para trabajar en esto.
19:10 <@hezekiah> Entonces vamos a dejar a todos boquiabiertos. :)
19:10 <@hezekiah> Sí. ¿Y cómo llega el pan a la mesa cuando haces eso?
19:10 <@hezekiah> El código GPL no paga bien. ;-)
19:10 < jrand0m> je
19:11 <@hezekiah> En cuanto a psyc... déjame ponerlo así:
19:11 <@hezekiah> La primera vez que oí hablar de ello fue cuando nos enviaste un correo 	al respecto.
19:11 < jrand0m> mierda, yo no fui quien lo encontró :)
19:11 <@hezekiah> Sin embargo, IRC es probablemente uno de los (si no /el/ 	más) prolíficos protocolos de chat que existen.
19:11 <@hezekiah> La gente querrá aplicaciones de IRC MUCHO antes de siquiera /saber/ 	qué es psyc.
19:11 <@hezekiah> jrand0m: Ups. Perdón. Olvidé ese detalle. :)
19:12 < jrand0m> no según psyc.  su historia se remonta al 86, creo
19:12 <@hezekiah> El punto es que la superioridad del protocolo no es 	realmente tan relevante como quién lo usa.
19:12 <@hezekiah> Su _historia_ puede remontarse tanto.
19:12 <@hezekiah> Pero ¿cuánta gente _usa_ Psyc?
19:12 < jeremiah> sí, si han estado por ahí desde un año después de que yo nací 	(ejem) y aún no son tan grandes
19:12 <@hezekiah> Mi punto es que, incluso si es un mejor protocolo, la mayoría 	de la gente _usa_ IRC.
19:13 <@hezekiah> Podemos hacer la mejor red I2P del planeta ...
19:13 -!- Ehud [logger@anon.iip] ha salido [Tiempo de espera de ping]
19:14 < jeremiah> ¿alguien puede explicar brevemente por qué nos importa? Pensé que IRC 	sería solo una posible aplicación, pero que la red es flexible para 	admitir también psyc si se quisiera
19:14 <@hezekiah> Correcto.
19:14 <@hezekiah> Se puede hacer psyc ...
19:14 <@hezekiah> ... pero digo que deberíamos hacer IRC primero porque más 	gente lo usa.

19:14 <@hezekiah> jrand0m, podemos crear una gran red I2P, pero la gente no la usará a menos que tenga algo que quieran.
19:14 < jrand0m> jeremiah> la razón por la que psyc es interesante es que quizá queramos implementar IRC en la misma línea en que funciona psyc
19:15 <@hezekiah> Por lo tanto deberíamos proporcionarles una 'killer-app' (aplicación estrella).
19:15 < jeremiah> ok
19:15 < jrand0m> correcto, IIP es el Invisible IRC Project, y permitirá a la gente ejecutar IRC
19:16 < jrand0m> sin servidor central (ni ningún servidor, de hecho), queda mucho por pensar para averiguar cómo funcionará IRC. psyc tiene una posible respuesta para eso
19:16 < jrand0m> aunque hay otras
19:17 <@hezekiah> Como dije, psyc podría funcionar mejor, pero la gente quiere usar IRC, no psyc.
19:17 < jrand0m> y lo harán
19:17 < jrand0m> usarán IRC
19:17 <@hezekiah> ¡Todo es cuestión de marketing, baby! ;-)
19:17 < jeremiah> Intentaré leer la especificación y algo de material sobre psyc esta noche
19:17 < jrand0m> eso
19:17 <@hezekiah> lol
19:17 < jeremiah> ¿Planeamos reunirnos a las 5:00 UTC mañana?
19:17 <@hezekiah> ¿No?
19:18 < jeremiah> o cuando sea
19:18 < jrand0m> Estoy en iip 24x7 :)
19:18 < jeremiah> sí, pero yo como
19:18 <@hezekiah> jrand0m: Me di cuenta.
19:18 < jrand0m> ¿05:00 utc o 17:00 utc?
19:18 <@hezekiah> jeremiah: ¡LOL!
19:18 <@hezekiah> Pues la reunión iip-dev comienza oficialmente a las 21:00 UTC.
19:18 -!- Ehud [~logger@anon.iip] se ha unido a #iip-dev
19:19 < jeremiah> ok, solo dije 05:00 UTC porque estaba hablando por hablar
19:19 < jeremiah> ¿Dónde está mids?
19:19 <@hezekiah> mids se fue del proyecto por un tiempo.
19:19 <@hezekiah> ¿No estuviste allí hace unas reuniones?
19:19 < jeremiah> ok
19:19 < jeremiah> supongo que no
19:19 <@hezekiah> Tuvimos una especie de fiesta de despedida como parte del orden del día.
19:19 < jeremiah> oh
19:20 <@hezekiah> OK ...
19:20 <@hezekiah> ¿Queda algo en la agenda?
19:20  * jrand0m no tiene nada más en la mía
19:20 < jeremiah> sobre psyc:
19:20 < jeremiah> si esto es una característica de psyc, sé que lo mencionaste hace un tiempo
19:20  * hezekiah nunca tuvo una agenda en primer lugar
19:21 <@hezekiah> pace
19:21 <@hezekiah> place
19:21 < jeremiah> No creo que hacer que cada usuario envíe un mensaje a cada otro usuario en la sala sea una idea inteligente
19:21 <@hezekiah> ¡Eso es!
19:21 < jrand0m> jeremiah> entonces ¿tendrías pseudoservidores redundantes designados que redistribuyan los mensajes?
19:21 < jrand0m> (pseudoservidores = pares en el canal que tienen la lista de usuarios)
19:21 < jeremiah> Tampoco creo que el 'broadcasting' sea tan inteligente, pero eso

parece que requerirá _mucho_ ancho de banda para un usuario dado que quizá esté en
	un módem, y con la latencia de enviar, digamos... 20 mensajes por separado
	arruinaría la conversación
19:21 < jeremiah> No sé cuál es la mejor solución, quizá esa sería una
19:22 < jeremiah> Creo que la mensajería directa sería buena si la quisieras,
	pero hay casos en los que probablemente no es tan importante
19:22 <@hezekiah> El mensaje tendría que estar firmado con la clave privada del autor
	para garantizar la autenticidad.
19:22 <@hezekiah> Aunque este tema no importará por bastante tiempo todavía,
	creo que jeremiah tiene razón
19:22 < jrand0m> hezekiah> eso requiere que los usuarios quieran una comunicación demostrable :)
19:23 < jrand0m> definitivamente.
19:23 <@hezekiah> Si tuviera que enviar un mensaje a 100 usuarios en un canal ...
19:23 < jeremiah> aunque mi mensaje promedio son solo unos pocos cientos de bytes,
	así que enviarlo a cientos de usuarios quizá no sea tan difícil
19:23 <@hezekiah> ... bueno, mi conversación sería /muy/ lenta.
19:23 < jeremiah> especialmente si no esperaras una respuesta
19:23 <@hezekiah> 20K para enviar un mensaje.
19:23 <@hezekiah> No lo creo. :)
19:23 < jrand0m> bueno, si hay 100 usuarios en un canal, *alguien* tiene
	que enviar 100 mensajes
19:23 < jeremiah> ¿son 20k?
19:23 < jeremiah> ah, cierto
19:23 <@hezekiah> 200 usuarios
19:24 < jeremiah> hmm
19:24 < jeremiah> ¿no serían buenos los router para eso?
19:24 < jeremiah> podemos asumir con cierta seguridad que tienen un ancho de banda decente,
	¿no?
19:24 <@hezekiah> Pensé que cada persona tenía una 'implementación de router'
19:24 < jrand0m> no realmente.  si hay relés, el mecanismo de nominación
	tiene que tener eso en cuenta
19:24 < jrand0m> sí, hezekiah
19:24 < jeremiah> no he leído la especificación
19:25 < jrand0m> un router es tu router local
19:25 <@hezekiah> ¡Uf!
19:25 <@hezekiah> ¡Sigo confundiendo sus nicks!
19:25 <@hezekiah> lol
19:25 < jrand0m> jeje
19:25 <@hezekiah> Em ... ¿a dónde se fue nop?
19:25 <@hezekiah> Oh.
19:26 <@hezekiah> Sigue aquí.
19:26 <@hezekiah> Por un momento pensé que se había ido,
19:26 < jrand0m> pero jeremiah tiene razón, psyc tiene algunas ideas que quizá queramos
	considerar, aunque quizá queramos rechazarlas
19:26 <@hezekiah> Primero pongamos la red a funcionar.
19:26  * jrand0m brinda por eso
19:26 <@hezekiah> Si estiras tu visión hasta la meta, tropezarás
	con la piedra que está a 3 pulgadas frente a ti.
19:27  * jeremiah se siente inspirado
19:27 <@hezekiah> lol
19:27 < jrand0m> Creo que sería realmente genial si pudiéramos proponernos revisar
	la especificación de la red para la próxima semana, enviando correos a iip-dev cuando
	alguien tenga ideas o comentarios.  ¿Estoy fuera de mí?
19:27 <@hezekiah> ¿nop? ¿Tienes algo más que añadir a la agenda,
	o levantamos la sesión?
19:27 <@hezekiah> jrand0m: Bueno, no sé si podría leer todo eso para
	la próxima semana, pero puedo intentarlo. :)
19:27 < jrand0m> je
19:28 < jrand0m> son 15 páginas agotadoras ;)
19:28 <@hezekiah> ¿15 páginas?
19:28 <@hezekiah> ¡Parecía más bien 120!
19:29 < jrand0m> je, bueno, depende de tu resolución, supongo ;)
19:29 < jeremiah> tiene muchas anclas ahí, hace que parezca
	que es enorme
19:29 < jrand0m> jeje
19:29 <@hezekiah> ¡El lado izquierdo tiene MUCHOS más de 15 enlaces, amigo!
19:29 <@hezekiah> ¡Confiesa!
19:29 <@hezekiah> Son más de 15. :)
19:29 <@hezekiah> ¡Oh!
19:29 <@hezekiah> ¡Esas no son páginas! ¡Solo son anclas!
19:29 <@hezekiah> ¡Estoy salvado!
19:30  * hezekiah se siente como un marinero recién rescatado de ahogarse
19:30 < jeremiah> clase, pasen al volumen 4 capítulo 2 Estructura de Bytes del Mensaje
19:30 < jrand0m> lol
19:30 <@hezekiah> lol
19:30 <@nop> se levanta la sesión
19:30 <@hezekiah> ¡*baf*!
19:30 <@hezekiah> La próxima semana, 21:00 UTC, mismo lugar.
19:30 <@hezekiah> Nos vemos allí. :)
19:30 < jeremiah> nos vemos --- Log closed Tue Jul 15 19:30:51 2003 </div>
