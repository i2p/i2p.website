---
title: "Réunion des développeurs I2P, 5 août 2003"
date: 2003-08-05
author: "nop"
description: "52nd I2P dev meeting covering Java development status, crypto updates, and SDK progress"
categories: ["meeting"]
---

<h2 id="quick-recap">Quick recap</h2>

<p class="attendees-inline"><strong>Present:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Meeting Log</h2>

<div class="irc-log"> <nop>	ok, meeting started <nop>	what's on the agenda -->	logger (logger@anon.iip) has joined #iip-dev -->	Anon02 (~anon@anon.iip) has joined #iip-dev <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	Welcome to the Nth iip-dev meeting. <hezekiah>	What's on the agenda? <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	synced to a NTP stratum 2 :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) has joined #iip-dev <hezekiah>	Just synced to NIST. :) <mihi>	this sync does not help w/ iip delays ;) <jrand0m>	nop: things I want to see covered: java dev status, java crypto 	  status, python dev status, sdk status, naming service <hezekiah>	(We're going into the naming service _already_?) <jrand0m>	not design you wanker, thats co's schpeel.  just talk about stuff 	  if there's stuff to talk about. <hezekiah>	Ah *	jrand0m puts LART away <jrand0m>	anything else on the agenda? <jrand0m>	or shall we dig in? <hezekiah>	Well, I can't think of anything else to add. <hezekiah>	Ah! <hezekiah>	Oh! <jrand0m>	ok.  java dev status: <hezekiah>	Good. <--	mrflibble has quit (Ping timeout) <nop>	ok <nop>	agenda <nop>	1) Welcome <jrand0m>	as of today, there is a java client API with a stub java router 	  that can talk to each other.  in addition, there is an application called ATalk 	  allowing anonymous IM + file transfer. <nop>	2) IIP 1.1 blackouts <nop>	3) I2P <nop>	4) The End with comments and stuff *	jrand0m goes back to corner <nop>	sorry 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah gives jrand0m a dunce hat to wear in 	  the corner. ;-) <nop>	sorry about that <nop>	didn't see you started there <nop>	maybe I should go in corner <hezekiah>	lol <jrand0m>	no worry.  item 1) *	hezekiah hands nop a dunce hat too. :) <nop>	ok welcome everybuddy <nop>	blah blah <nop>	2) IIP 1.1 blackouts -->	mrflibble (mrflibble@anon.iip) has joined #iip-dev <hezekiah>	52nd iip-dev meeting and all that good rot! <nop>	the server recently had some issues with the hard drive sectors and has 	  been replaced <nop>	I plan to be moving the darn server into a more stable environment with 	  redundancy <nop>	and possibly lend out control of multiple ircd servers <nop>	dunno <nop>	that's something to be discussed <--	Anon02 has quit (EOF From client) <nop>	hopefully our servers should stay up now since the harddrive was replaced <nop>	sorry about the inconvenience folks <nop>	3) I2P - Jrand0m take it away <nop>	come out of the corner jrand0m *	hezekiah goes over to the corner, pulls jrand0m off his chair, drags him 	  to the podium, takes away his dunce hat, and hands him the mic. *	nop goes into that corner to fill his place <hezekiah>	lol! <jrand0m>	sorry, back *	nop grabs dunce hat from hezekiah *	nop puts it on his head *	nop applauds for jrand0m *	jrand0m just watches the show <jrand0m>	er... um ok <hezekiah>	jrand0m: i2p, java status, etc. Talk man! <jrand0m>	so, as of today, there is a java client API with a stub java 	  router that can talk to each other.  in addition, there is an application called 	  ATalk allowing anonymous IM + file transfer. <hezekiah>	File transfer already!? <jrand0m>	si sr <hezekiah>	Wow. <hezekiah>	I'm sure behind the times. <jrand0m>	but not the most graceful <hezekiah>	lol <jrand0m>	it takes a file and tosses it in a message <hezekiah>	Ouch. <nop>	how long did 1.8 mb local transfer take? <jrand0m>	I've tested with a 4K file and a 1.8Mb file <jrand0m>	a few seconds <nop>	nice <nop>	:) <hezekiah>	Does the java stuff do real encryption yet, or does it still 	  fake that? <nop>	fake <nop>	even I know that <nop>	:) <jrand0m>	I warmed it up by talking to myself first [e.g. one window to 	  another, saying hi] so it didn't deal with the overhead of the first elg <jrand0m>	right, its faked largely <thecrypto>	most of the encryption is fake <thecrypto>	that's being worked on though <hezekiah>	Of course. :) <jrand0m>	definitely. <jrand0m>	on that front, wanna give us an update thecrypto? <thecrypto>	well, right now i'm done with ElGamal and SHA256 <thecrypto>	right now I'm working on generating primes for DSA <thecrypto>	I'll send out 5 and then we can just pick one <hezekiah>	nop: Didn't you have prime(s) coming for use with DSA? <thecrypto>	We also have some benchmarks on ElGamal and SHA256 <thecrypto>	And they are all fast <jrand0m>	latest benchmarks w/ elg: <jrand0m>	Key Generation Time Average: 4437	total: 443759	min: 	  872	   max: 21110	   Keygen/second: 0 <jrand0m>	Encryption Time Average    : 356	total: 35657	min: 	  431	   max: 611	   Encryption Bps: 179 <jrand0m>	Decryption Time Average    : 983	total: 98347	min: 	  881	   max: 2143	   Decryption Bps: 65

<hezekiah>	min and max: are they in seconds? <jrand0m>	note that the Bps isn't really useful, as we only encrypt/decrypt 	  64 bytes <thecrypto>	ms <jrand0m>	no, sorry, those are all milliseconds <hezekiah>	Cool. :) <hezekiah>	And this is done in java? <thecrypto>	yes <thecrypto>	pure java <hezekiah>	OK. I am officiall impressed. :) <jrand0m>	100%.  P4 1.8 <thecrypto>	they are about the same on my 800 Mhz <hezekiah>	How can I do the same tests? <jrand0m>	sha256 benchmark: <jrand0m>	Short Message Time Average  : 0 total: 0	min: 0	max: 	  0  Bps: NaN <jrand0m>	Medium Message Time Average : 1 total: 130	min: 0	max: 	  10 Bps: 7876923 <jrand0m>	Long Message Time Average   : 146	total: 14641	min: 	  130	   max: 270	   Bps: 83037 <thecrypto>	run the ElGamalBench program <hezekiah>	OK. <hezekiah>	I'll go find it. <jrand0m>	(short size: ~10 bytes, medium ~10KB, long ~ 1MB) <jrand0m>	java -cp i2p.jar ElGamalBench <jrand0m>	(after running "ant all") <hezekiah>	jrand0m: Thanks. :) <jrand0m>	np <thecrypto>	The NaN thing means it's so fast that we end up dividing by 0 	  it's so fast :) <hezekiah>	What's the sha bench? <jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip) has joined #iip-dev <hezekiah>	OK. <jrand0m>	we'll probably want to move those to be main() methods of the 	  associated engines, but they're good where they are atm <hezekiah>	Let's see how fast all this is on an AMD K6-2 333MHz (which is 	  a chip not well know for its integer math.) <jrand0m>	heh <jrand0m>	ok so we have DSA and AES left, right? <jrand0m>	this is all wikked thecrypto.  nice work. <thecrypto>	yup <jrand0m>	can I nag you for an ETA on the other two?  ;) <hezekiah>	If this is anywhere near as fast on my box as it is on yours, 	  you have to show me how you do that. ;-) <thecrypto>	DSA should be done almost as soon as i have primes ready <nop>	hezekiah have you tried the sslcrypto for python <thecrypto>	copying some code around from the prime generator and things like 	  that and it's done <nop>	the one off that link <hezekiah>	nop: sslcrypto won't do us any good. <hezekiah>	nop: It doesn't implment ElGamal _or_ AES _or_ sha256. <thecrypto>	AES is mostly done except that there is some error somewhere that 	  i'm still trying to pick out and destroy, once i have that, it'll be done <jrand0m>	thecrypto> so by friday, DSA keygen, sign, verify, and AES encrypt, 	  decrypt for arbitrary size inputs? <nop>	the one on McNab's site does not? <thecrypto>	yeah <nop>	darn <thecrypto>	should be friday <thecrypto>	most likey thursday <jrand0m>	thecrypto> does that include the UnsignedBigInteger stuff? <thecrypto>	i'll be missing next weeks meeting because of summer camp, and 	  i'll be back after that <thecrypto>	jrand0m: prolly not <jrand0m>	ok. <jrand0m>	so for the time being, interoperability between java and python 	  is b0rked. <jrand0m>	for crypto, that is. ---	Notify: jeremiah is online (anon.iip). -->	jeremiah (~chatzilla@anon.iip) has joined #iip-dev <jrand0m>	(aka for signatures, keys, encryption, and decryption)

<nop>	hmm maybe we should focus more on C/C++ <thecrypto>	well, once we get it working completely we can then make sure 	  both java and python can speak to each other <jrand0m>	while you're out I'll look into the unsigned stuff. <jeremiah>	can someone email me a backlog? jeremiah@kingprimate.com <hezekiah>	jeremiah: Give me a minute. :) <jrand0m>	nop> do we have devs for C/C++? <nop>	I have one guy yes <nop>	and Hezekiah we know could do it <jrand0m>	or perhaps we can get a python dev status update from hezekiah + 	  jeremiah to see when we'll have more people for the c/c++ dev <jrand0m>	right, of course.  but hez+jeremiah are working on python atm 	  (right?) <hezekiah>	Yeah. <--	mrflibble has quit (Ping timeout) <hezekiah>	I'm sort of giving poor jeremiah lots of trouble. <nop>	I was just saying if python won't be fast speeds <hezekiah>	Python is mainly for me to understand this network. <nop>	ahh <hezekiah>	Once, I get it to basically follow the complete spec, I intend 	  to hand it off to jeremiah to do with as he sees fit. <hezekiah>	It's not meant to be a killer implementation of the spec. <hezekiah>	(If I wanted that, I'd use C++.) <jeremiah>	well there aren't any really processor intensive parts of the app, 	  iirc, aside from crypto, and ideally that will be handled in C anyways, right? <jrand0m>	sure jeremiah.all depends on the app -->	mrflibble (mrflibble@anon.iip) has joined #iip-dev <hezekiah>	jeremiah: In theory. <jrand0m>	so where are we on the python side?  client api, local only 	  router, etc? <jeremiah>	the python implementation will also let us know what optimizations 	  we could make from the start... I'd like to keep it up to date or, possibly, 	  ahead of the C implementation as I can <hezekiah>	jrand0m: OK. Here's what I've got. <hezekiah>	In _theory_ the router should be able to handle all non-admin 	  messages from a client. <hezekiah>	However, I don't have client yet, so I haven't been able to debug 	  it (i.e. there are still bugs.) <hezekiah>	I'm working on the client right now. <jrand0m>	'k.  if you can disable signature verification, we should be able 	  to run the java client against it now <hezekiah>	I'm hoping to have that done except for admin messages in a day 	  or two. <jrand0m>	we can test that out after the meeting <hezekiah>	jrand0m: OK. <jeremiah>	I've been dealing with real-world stuff mostly since the last 	  meeting, I can work on the client API, just been trying to sync my thinking 	  with hezekiah's <jrand0m>	cool <hezekiah>	jeremiah: You know what, just wait. <hezekiah>	jeremiah: I'm probably throwing in too much new stuff for you to 	  deal with right now. <jeremiah>	hezekiah: right, what I was going to say is that you should 	  probably just go ahead and implement the base stuff <hezekiah>	jeremiah: In a little while, it will be stabalized and you can 	  start refining it. (There are lots of TODO comments that need help.) <jeremiah>	and then I can extend it later once I get the picture <hezekiah>	Exactly. <hezekiah>	You get to maintain all this code. :) <jrand0m>	cool.  so eta 1-2 weeks for a working python router + client api? <hezekiah>	I'm going on vacation next week so probably. <hezekiah>	Are we going to have more details on router to router soon? <jrand0m>	no. <jrand0m>	well, yes. <jrand0m>	but no. <hezekiah>	lol <jeremiah>	hezekiah: how long is the vacation? <hezekiah>	1 week. <jeremiah>	ok <jrand0m>	(aka as soon as the SDK goes out, 100% of my time goes into I2NP) <hezekiah>	I'm hoping to have all non-admin functionality written before I 	  go on vacation <hezekiah>	. <jrand0m>	but then soon after you get back you're off to college, right? <hezekiah>	I2NP? <hezekiah>	Right. <jrand0m>	network proto <hezekiah>	I have about 1 week after vacation. <hezekiah>	Then I'm gone. <hezekiah>	And my free time drops like a stone. <jrand0m>	so that 1 week should only be debugging <jeremiah>	I can work on the code while hez is gone though <jrand0m>	word <jrand0m>	whats your summer look like jeremiah? <hezekiah>	jeremiah: Perhaps you can get those admin functions working?

<thecrypto>	j'aurai encore un mois après mon retour de vacances pour travailler 	  sur des trucs
<jrand0m>	avoir une vie, ou être comme le reste d'entre nous, des l00sers ?  :)
<jeremiah>	peut-être
<hezekiah>	100sers?
<hezekiah>	Qu'est-ce qu'un 100ser ?
<jeremiah>	je pars à la fac le 22, à part ça je peux dev
<mihi>	hezekiah : un loser
<jeremiah>	et la dernière semaine avant mon départ, tous mes amis seront partis... donc 	  je peux passer en mode hyperdev
<hezekiah>	mihi : Ah !
<jrand0m>	héhé
<hezekiah>	OK. Alors, on en était où à l'ordre du jour ?
<hezekiah>	c.-à-d. Qu'est-ce qui vient ensuite ?
<jrand0m>	statut du SDK (kit de développement logiciel)
<jrand0m>	SDK == une impl cliente, une impl de router local uniquement, une appli, et de la doc.
<jrand0m>	J'aimerais sortir ça d'ici mardi prochain.
<hezekiah>	jeremiah : Ce backlog est en route. Désolé je t'avais oublié là. :)
<jeremiah>	merci
<jrand0m>	ok, co n'est pas là, donc le truc du service de nommage est p'têt un peu 	  à côté de la plaque
<jrand0m>	on pourra discuter du service de nommage après qu'il publie des specs ou 	  quand il sera là
<jrand0m>	ok, c'est tout pour les trucs I2P
<jrand0m>	quelqu'un a autre chose pour I2P, ou on passe à :
<nop> 4) La fin avec 	  des commentaires et tout
<hezekiah>	Je ne vois rien.
<jrand0m>	Je suppose que tout le monde a vu 	  http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html ?
<thecrypto>	pas ici
<jrand0m>	(nop l'a posté ici plus tôt)
<hezekiah>	Le truc à propos du gars qui s'est fait arrêter pour avoir mis un lien 	  vers un site de fabrication de bombes ?
<jrand0m>	oui
<jrand0m>	La pertinence par rapport au besoin de mettre I2P en place ASAP devrait être évidente ;)
<hezekiah>	OK ! jeremiah, ces logs sont envoyés maintenant.
<jeremiah>	merci
<jrand0m>	quelqu'un a des questions / commentaires / pensées / frisbees, 	  ou on bat le record de la réunion la plus courte ?
*	thecrypto lance un frisbee <--	logger a quitté (Ping timeout)
<jrand0m>	mince, vous êtes vachement silencieux aujourd'hui ;)
<mihi>	question :
<mihi>	où les non-devs peuvent-ils récupérer votre code Java ?
<jrand0m>	si sr?
<thecrypto>	pas encore
<mihi>	404
<jrand0m>	ce sera disponible une fois qu'on sera prêts pour une release.  aka les 	  sources sortiront avec le SDK
<jrand0m>	heh
<jrand0m>	ouais, on n'utilise pas SF
<hezekiah>	nop : Est-ce possible d'avoir un CVS anonyme qui fonctionne un de ces jours ?
<hezekiah>	temps ?
<--	mrflibble a quitté (Ping timeout)
<nop>	eh bien, j'ouvrirais un port non standard
<jrand0m>	hezekiah> on aura ça une fois que le code aura la licence GPL dessus
<nop>	mais je bosse sur viewcvs
<jrand0m>	aka pas maintenant puisque le doc GPL n'a pas encore été ajouté au code
<hezekiah>	jrand0m : C'est dans tous les répertoires de code Python et tous les 	  fichiers source Python précisent une licence sous GPL-2.
<jrand0m>	hezekiah> c'est sur cathedral ?
<hezekiah>	Oui.
<jrand0m>	ah ouais.  i2p/core/code/python ?  ou un module différent ?
*	jrand0m ne l'a pas vu là-dedans
<hezekiah>	Chaque répertoire de code Python a un fichier COPYING avec la 	  GPL-2 et chaque fichier source a la licence définie à GPL-2
<hezekiah>	C'est i2p/router/python et i2p/api/python
<jrand0m>	'k
<jrand0m>	donc, ouais, d'ici mardi prochain on aura le SDK + l'accès public aux sources.
<hezekiah>	Cool.
<hezekiah>	Ou comme tu aimes dire, wikked. ;-)
<jrand0m>	heh
<jrand0m>	nada mas?
<hezekiah>	nada mas ? Qu'est-ce que ça veut dire !?
<jeremiah>	rien de plus
*	jrand0m suggère que tu apprennes un peu d'espanol en universidad
-->	mrflibble (mrflibble@anon.iip) a rejoint #iip-dev
<hezekiah>	Des questions, quelqu'un ?
<hezekiah>	Une fois !
<--	ptm (~ptm@anon.iip) a quitté #iip-dev (ptm)
<hezekiah>	Deux fois !
<--	mrflibble a quitté (mr. flibble dit « game over boys »)
<hezekiah>	Parlez maintenant... ou attendez jusqu'à ce que vous ayez envie de parler plus tard !
<thecrypto>	ok, je vais optimiser l'ElGamal encore plus, donc attendez-vous 	  à des benches ElGamal encore plus rapides à l'avenir
<jrand0m>	s'il te plaît, concentre-toi sur DSA et AES avant de tuner... s'te plaaaaaît :)
<thecrypto>	je vais le faire
<hezekiah>	La raison pour laquelle il fait ça, c'est parce que je cause de nouveau 	  des problèmes aux gens. ;-)
<thecrypto>	je fabrique des nombres premiers DSA
-->	mrflibble (mrflibble@anon.iip) a rejoint #iip-dev
<thecrypto>	eh bien, au moins je fais le programme pour fabriquer des nombres premiers DSA en ce moment
<hezekiah>	ElGamal en Java n'aime pas un AMD K-6 II 333 MHz.
<hezekiah>	OK.
<hezekiah>	Le tour de questions est terminé !
<jrand0m>	ok hez, on a fini.  tu veux faire un powow pour faire marcher le client Java 	  et le router Python ?
<hezekiah>	À la semaine prochaine, citoyens !
*	hezekiah abat le *baf*er
</div>
