---
title: "Réunion des développeurs I2P, 19 août 2003"
date: 2003-08-19
author: "jrand0m"
description: "54e réunion des développeurs I2P portant sur les mises à jour du SDK, la revue d'I2NP, les avancées en cryptographie et l'état d'avancement du développement"
categories: ["meeting"]
---

<h2 id="quick-recap">Récapitulatif rapide</h2>

<p class="attendees-inline"><strong>Présents:</strong> cohesion, hezekiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Journal de réunion</h2>

<div class="irc-log"> --- Journal ouvert mar. 19 août 2003 16:56:12 17:00 -!- logger [logger@anon.iip] a rejoint #iip-dev 17:00 -!- Sujet pour #iip-dev: Les réunions hebdomadaires de développement IIP, et d'autres 	 conversations entre développeurs, ont lieu ici. 17:00 [Utilisateurs #iip-dev] 17:00 [ cohesion] [ leenookx  ] [ mihi] [ shardy_  ] [ UserXClone] 17:00 [ Ehud    ] [ logger    ] [ nop ] [ thecrypto] [ velour    ] 17:00 [ hezekiah] [ lonelynerd] [ Rain] [ UserX    ] [ WinBear   ] 17:00 -!- Irssi: #iip-dev: Total de 15 pseudos [0 ops, 0 halfops, 0 voices, 15 normaux] 17:00 -!- Irssi: La connexion à #iip-dev a été synchronisée en 7 s 17:00 < hezekiah> Super ! :) 17:00 < hezekiah> Les deux loggers sont en place. :) 17:01 < thecrypto> ouais ! 17:03 < hezekiah> Hmm ... 17:03 < hezekiah> Cette réunion était censée commencer il y a 3 minutes. 17:03 < hezekiah> Je me demande ce qui se passe. 17:04 < thecrypto> bon, qui est inactif 17:04 < hezekiah> jrand0m n'est même pas en ligne. 17:04 < hezekiah> nop est inactif depuis 15 minutes. 17:05 < nop> salut 17:05 < nop> désolé 17:05 < nop> Je suis super débordé au boulot 17:05 < mihi> [22:36] * jrand0m s'en va dîner mais je serai de retour d'ici 	 une demi-heure pour la réunion 17:05 -!- jrand0m [~jrandom@anon.iip] a rejoint #iip-dev 17:05 < hezekiah> Salut, jrand0m. 17:05 < nop> salut 17:05 < nop> ok, voilà le truc 17:05 < nop> Je ne peux pas me montrer sur IIP au travail en ce moment 17:05 < nop> donc je vous recontacte plus tard 17:05 < nop> je me suis fait remonter les bretelles hier à ce sujet 17:05 < nop> donc 17:05 < hezekiah> Bye, nop. 17:05 < thecrypto> bye 17:06 < nop> Je reste sur le canal 17:06 < nop> je serai juste discret :) 17:06 < hezekiah> jrand0m ? Puisque tu parles le plus ces jours-ci, y a-t-il 	 quelque chose que tu veux mettre à l'ordre du jour pour cette réunion ? 17:07 < jrand0m> de retour 17:08 < jrand0m> ok, les pâtes au pesto étaient bonnes. 17:08 < jrand0m> laissez-moi sortir des trucs façon ordre du jour 17:09 -!- Lookaround [~chatzilla@anon.iip] a rejoint #iip-dev 17:09 < jrand0m> x.1) modifs SDK i2cp x.2) revue i2np x.3) polling http 	 transport x.4) dev status x.5) todo x.6) plan pour les deux prochaines semaines 17:09 < jrand0m> (mettez x au numéro qui convient dans l'ordre du jour) 17:10 < thecrypto> tu es l'agenda 17:10 < hezekiah> jrand0m: Je n'ai rien à dire, et nop peut 17:10 < hezekiah> pas parler. 17:10 < jrand0m> lol 17:10 < hezekiah> UserX n'ajoutera probablement rien (il ne le fait 	 généralement pas), donc pour moi, c'est tout à toi. :0 17:10 < hezekiah> :) 17:10 < jrand0m> 'k. on loggue ? 17:10 < jrand0m> héhé 17:10 < hezekiah> Je loggue tout. 17:10 < jrand0m> cool. ok. 0.1) bienvenue. 17:10 < jrand0m> salut. 17:11 < jrand0m> 0.2) liste de diffusion 17:11 < jrand0m> la liste est hors service pour l'instant, de retour dès que possible. 	Vous le saurez quand ce sera le cas :) 17:11 < jrand0m> en attendant, le wiki ou utilisez IIP pour discuter. 17:11 < jrand0m> 1.1) i2cp sdk mods 17:12 < jrand0m> Le SDK a été mis à jour avec quelques corrections de bugs, plus 	 l'introduction de nouvelles choses dans la spéc. 17:12 < jrand0m> J'ai posté l'info sur la liste hier. 17:13 < jrand0m> hezekiah/thecrypto/jeremiah> des questions sur ce que j'ai posté, 	 ou des idées de plan pour implémenter les changements ? (ou d'autres 	 alternatives auxquelles je n'ai pas pensé ?) 17:13 < hezekiah> Je cours dans tous les sens pour préparer la fac. 17:13 < jrand0m> ok, compris. 17:13 < hezekiah> J'ai jeté un coup d'œil rapide à ce que tu as écrit, mais je n'ai pas 	 réellement regardé les changements de la spéc. 17:13 < jrand0m> il ne nous reste quasiment plus de ton temps, hein... 17:13 < hezekiah> Pas avant d'arriver à la fac. 17:14 < hezekiah> Une fois sur place, je serai probablement silencieux au 	 moins une semaine le temps de m'adapter. 17:14 < jrand0m> et une fois que tu y seras tu auras beaucoup à t'installer 	 (si je me souviens bien de quand je suis allé à l'école ;) 17:14 < jrand0m> héhé, clair. 17:14 < hezekiah> Ensuite, je devrais être un peu plus efficace et avoir 	 plus de temps pour pouvoir coder. 17:14 < jrand0m> cool 17:14 < thecrypto> je fais juste de la crypto, donc les structures de données sont 	 mon vrai souci; une fois que j'aurai terminé le mode CTS, je m'y mettrai 	 probablement 17:14 < hezekiah> Bref, c'est mon avis. 17:14 < jrand0m> excellent thecrypto 17:15 < jrand0m> ok, la bonne nouvelle c'est que le SDK fonctionne parfaitement 	 (les bugs trouvés par mihi ont été corrigés [yay mihi!]) sans la mise à jour 	 de la spéc. 17:15 -!- arsenic [~none@anon.iip] a rejoint #iip-dev 17:16 < jrand0m> ok, passons à 1.2) revue i2np 17:16 < jrand0m> quelqu'un a lu la doc ? 17:16 < jrand0m> ;) 17:16 < hezekiah> Pas moi, pas encore. 17:16 < hezekiah> Comme je l'ai dit, je suis actuellement comme une poule sans tête. 17:17 < hezekiah> Au fait jrand0m, on dirait que tu aimes envoyer des PDF. 17:17 < jrand0m> tout le monde peut lire les .swx openoffice ? 17:17 < hezekiah> Moi oui. 17:17 < jrand0m> [si oui, j'enverrai des swx] 17:17 -!- abesimpson [~k@anon.iip] a rejoint #iip-dev 17:17 < thecrypto> moi je peux 17:17 < hezekiah> Je ne peux pas chercher du texte dans un PDF avec KGhostView. 17:17 < hezekiah> Donc ça fait vraiment mal. 17:17 < jrand0m> c'est nul, hezekiah 17:17 -!- mrflibble [mrflibble@anon.iip] a rejoint #iip-dev 17:17 < hezekiah> La version Linux d'Adobe Acrobat n'est pas très conviviale non plus. 17:18 < jrand0m> ok, ce sera le format openoffice plutôt que PDF. 17:18 < hezekiah> Cool. 17:18 < jrand0m> euh, ok. i2np a quelques changements mineurs à la structure 	 LeaseSet (reflétant le changement i2cp posté plus tôt), mais à part ça, c'est 	 largement en place. 17:19 < hezekiah> jrand0m: Tous ces docs sont-ils dans le CVS de cathedral ? 17:19 < nop> oh 17:19 < nop> puis-je intervenir 17:19 < hezekiah> c.-à-d. des copies des fichiers PDF que tu as envoyés à la 	 liste, etc. 17:19 < hezekiah> nop: Vas-y. 17:19 < nop> c'est hors sujet mais important 17:19 -!- ChZEROHag [hag@anon.iip] a rejoint #iip-dev 17:19 < nop> IIP-dev et le mail sont un peu bancals en ce moment 17:19 < hezekiah> J'ai remarqué. 17:19 < nop> donc soyez indulgents un moment 17:20 < nop> on essaie de remettre ça en route 17:20 < nop> mais il y a SpamAssassin intégré 17:20 < nop> c'est la bonne nouvelle 17:20 < nop> :) 17:20 < nop> et plein d'autres fonctionnalités 17:20 < jrand0m> une estimation, nop, pour la liste ? 17:20  * ChZEROHag passe le nez 17:20 < jrand0m> (je sais que tu es occupé, je ne harcèle pas, je demande juste) 17:20 < nop> espérons d'ici demain 17:20 < jrand0m> cool 17:20 < nop> l'admin mail travaille dessus 17:21  * hezekiah note que jrand0m aime _vraiment_ la liste iip-dev. ;-) 17:21 < nop> haha 17:21 < hezekiah> Allez delta407 ! 17:21 < nop> bref 17:21 < jrand0m> il vaut mieux documenter les décisions publiquement, hezekiah ;) 17:21 < nop> retour à notre réunion habituelle 17:21 < jrand0m> héhé 17:21 -!- nop est maintenant connu sous le nom de nop_afk 17:21 < hezekiah> jrand0m: Alors où en étions-nous ? 17:21 < jrand0m> ok, pour répondre à ta question hezekiah> certaines y sont, 	 mais pas les dernières. Je passerai à la mise au format openoffice. 17:21 < jrand0m> plutôt que les PDFs 17:22 < hezekiah> OK. 17:22 < hezekiah> Ce serait vraiment cool si toute la doc était dans le CVS. 17:22 < jrand0m> carrément, et elles y seront 17:22 < hezekiah> Ainsi je n'aurai qu'à mettre à jour et je saurai que j'ai la dernière édition. 17:22 < jrand0m> (il y a trois brouillons qui ne le sont pas pour l'instant) 17:22 < hezekiah> (Au fait, un peu hors sujet, mais l'accès anonyme à 	 cathedral est-il déjà en place ?) 17:23 < jrand0m> pas encore. 17:23 < jrand0m> ok, d'ici vendredi, j'espère avoir une autre ébauche d'I2NP 	 en forme complète [c.-à-d. plus de ... pour les sections d'explication 	 Kademlia, et des détails d'implémentation d'exemple] 17:24 < jrand0m> il n'y a pas de changements significatifs. juste plus de 	 compléments qui clarifient. 17:24 < hezekiah> Génial. 17:24 < hezekiah> Y aura-t-il l'agencement en octets des structures de données 	 disponible dedans ? 17:24 < jrand0m> 1.3) I2P Polling HTTP Transport spec. 17:24 < jrand0m> non, les agencements en octets vont dans la spéc des structures 	 de données, qui devrait être convertie au format standard au lieu de html 17:25 < jrand0m> (bien qu'I2NP ait déjà tous les agencements en octets nécessaires) 17:25 < jrand0m> ((si tu la lisais *tousse* ;)) 17:25 < hezekiah> Bien. 17:25 < hezekiah> lol 17:25 < hezekiah> Désolé pour ça. 17:25 < hezekiah> Comme je l'ai dit, j'ai été vraiment occupé. 17:25 < jrand0m> héhé pas de souci, tu pars à la fac bientôt, tu es censé 	 faire la fête :) 17:25 < hezekiah> Faire la fête ? 17:25 < jrand0m> ok, 1.3) I2NP Polling HTTP Transport spec 17:25 < hezekiah> Hmm ... Je dois être juste un peu étrange. 17:25 < jrand0m> héhé 17:26 < jrand0m> ok, j'ai essayé d'envoyer ça plus tôt, mais je vais le committer 	 sous peu. c'est un protocole de transport rapide et sale qui s'intègre à I2NP 	 pour permettre aux routers d'envoyer des données dans les deux sens sans 	 connexions directes (p. ex. pare-feu, proxies, etc.) 17:27 < jrand0m> J'*espère* que quelqu'un pourra voir comment ça marche et 	 construire des transports similaires (p. ex. TCP bidirectionnel, UDP, HTTP direct, etc.) 17:27 -!- mihi [none@anon.iip] a quitté [Ping timeout] 17:27 < hezekiah> Hmm, eh bien je ne 17:27 < jrand0m> avant de soumettre I2NP à relecture, nous devons inclure 	 des transports d'exemple pour que les gens voient l'ensemble 17:27 < hezekiah> pense pas que _moi_ je construirai des transports de sitôt. ;-) 17:27 -!- WinBear_ [~WinBear@anon.iip] a rejoint #iip-dev 17:27 < hezekiah> TCP fonctionne pour Java et Python. 17:27 < hezekiah> (Au moins côté client-vers-router.) 17:27 < jrand0m> pas d'inquiétude, je le mets là comme todo pour ceux qui 	 veulent contribuer 17:28 < hezekiah> D'accord. 17:28 < jrand0m> oui, client-router a des exigences différentes de 	 router-router. 17:28 < jrand0m> ok, bref, 1.4) dev status 17:28 < jrand0m> où en est-on avec le CBC, thecrypto ? 17:28 < thecrypto> CBC est commité 17:28 < jrand0m> w00000t 17:28 < thecrypto> CTS est presque fini 17:28 < hezekiah> thecrypto: C'est quoi CTS ? 17:29 < thecrypto> je dois juste trouver comment l'implémenter proprement 17:29 < jrand0m> CTS, c'est le CipherText Stealing (technique permettant d'ajuster la longueur sans bourrage) :) 17:29 < hezekiah> Ah ! 17:29 < thecrypto> CipherText Stealing 17:29 -!- WinBear [WinBear@anon.iip] a quitté [EOF From client] 17:29 < jrand0m> as-tu récupéré la référence de nop à ce sujet ? 17:29 < hezekiah> OK. On utilise CBC avec CTS au lieu de padding. 17:29 < hezekiah> Hmm. 17:29 < thecrypto> en gros, ça rend le message exactement de la bonne longueur 17:29 < jrand0m> est-ce faisable côté Python, hezekiah ? 17:29 < hezekiah> Je vais peut-être devoir secouer la lib crypto Python que 	 j'utilise pour qu'elle utilise correctement CTS. 17:30 < hezekiah> J'ai toujours préféré CTS au padding, mais je ne sais pas 	 ce que fait PyCrypt. 17:30 < jrand0m> que peut faire Python nativement pour permettre de retrouver 	 exactement la taille du message ? 17:30 < thecrypto> il suffit de changer la façon de traiter les deux derniers 	 blocs 17:30 < hezekiah> J'ai le sentiment que cette bibliothèque va avoir droit à une sérieuse 	 réécriture. 17:30 < hezekiah> jrand0m: Le truc CBC en Python est transparent. Tu envoies 	 juste le tampon à la fonction encrypt de l'objet AES. 17:31 < hezekiah> Ça recrache du texte chiffré.

17:31 < hezekiah> Fin de l'histoire.
17:31 < jrand0m> does D(E(data,key),key) == data, byte for byte, exact 	 same size?
17:31 < hezekiah> Donc s'il a l'idée saugrenue d'utiliser du bourrage au lieu de CTS, 	 il faudra peut-être que je mette les mains dans le cambouis et que je corrige ça.
17:31 < jrand0m> (quelle que soit la taille d'entrée ?)
17:31 -!- mihi [~none@anon.iip] a rejoint #iip-dev
17:31 < hezekiah> jrand0m: Oui. Ça devrait.
17:31 < jrand0m> hezekiah> si tu pouvais vérifier exactement quel algorithme il 	 utilise pour faire le bourrage, ce serait top
17:32 < hezekiah> D'accord.
17:32  * jrand0m hésite à exiger une modif d'une bibliothèque crypto Python si 	 la lib utilise déjà un mécanisme standard et utile
17:32 < hezekiah> D'une manière ou d'une autre, CBC avec CTS semble bien.
17:32 < hezekiah> jrand0m: Cette lib crypto Python pue.
17:32 < jrand0m> heh 'k
17:33 < thecrypto> je dois juste calculer comment bidouiller les deux blocs
17:33 < hezekiah> jrand0m: ElGamal devra être entièrement réécrit en 	 C rien que pour le rendre assez rapide à utiliser.
17:33 < jrand0m> hezekiah> quel est le benchmark pour l'elg Python de 256 octets? 	 c'est fait une seule fois par comm dest-dest...
17:34 < jrand0m> (si tu sais ça de tête, bien sûr)
17:34 < hezekiah> Je devrais le tester.
17:34 < hezekiah> Le chiffrement ne prend qu'une seconde ou deux je crois
17:34 < jrand0m> < 5 s, < 2 s, > 10 s, > 30 s?
17:34 < thecrypto> je vais probablement bosser un peu dessus
17:34 < hezekiah> Le déchiffrement est peut-être quelque part entre 5 et 10 secondes.
17:34 < jrand0m> cool.
17:35 < jrand0m> hezekiah> tu as parlé avec jeremiah ou tu as des 	 nouvelles sur l'état de l'API client Python ?
17:35 < hezekiah> thecrypto: Tout ce que tu devrais avoir à faire, 	 c'est écrire un module C qui fonctionne avec Python.
17:35 < hezekiah> Je n'ai aucune idée de ce qu'il a fait.
17:35 < hezekiah> Je ne lui ai pas parlé depuis mon retour.
17:35 < jrand0m> 'k
17:35 < jrand0m> d'autres points d'état côté dev ?
17:36 < hezekiah> Euh, pas vraiment de mon côté.
17:36 < hezekiah> J'ai déjà expliqué ma dispo actuelle.
17:36 < jrand0m> ok.  compris
17:36 < hezekiah> Mes seuls plans sont de mettre en place l'API C et de remettre le router 	 Python conforme à la spec.
17:37 < jrand0m> 'k
17:37 < hezekiah> Oh mon dieu !
17:37 < jrand0m> 1.4) à faire
17:37 < jrand0m> si sr?
17:37 < hezekiah> La lib crypto Python n'implémente ni CTS ni le bourrage !
17:37 < hezekiah> Je vais devoir le faire manuellement.
17:37 < jrand0m> hmm?  il exige que les données soient mod 16 octets?
17:37 < hezekiah> Oui.
17:38 < jrand0m> heh
17:38 < jrand0m> tant pis.
17:38 < hezekiah> Actuellement le router Python utilise du bourrage.
17:38 < jrand0m> ok.  voici quelques éléments en suspens à faire.
17:38 < hezekiah> Je m'en souviens maintenant.
17:38 < hezekiah> Bon, lais
17:38 < hezekiah> soyons francs sur un point.
17:38 < hezekiah> Le router Python n'est pas vraiment destiné à être utilisé.
17:39 < hezekiah> Il est principalement destiné à me rendre très familier avec la 	 spec et il accomplit aussi autre chose :
17:39 < hezekiah> Il oblige le router Java à se conformer _exactement_ à la spec.
17:39 < jrand0m> deux objectifs très importants.
17:39 < hezekiah> Parfois le router Java ne se conforme pas tout à fait, et 	 là le router Python pousse des cris d'orfraie.
17:39 < hezekiah> Donc il n'a pas vraiment besoin d'être rapide ou stable.
17:39 < jrand0m> et je ne suis pas sûr qu'il ne sera jamais utilisé dans le sdk
17:39 < jrand0m> ouais.  exactement.
17:39 < jrand0m> l'API client Python, c'est autre chose par contre
17:39 < hezekiah> En revanche, l'API client Python doit être correcte.
17:40 < jrand0m> exactement.
17:40 < hezekiah> Mais ça, c'est le problème de jeremiah. :)
17:40 < hezekiah> Je lui ai laissé ça.
17:40 < jrand0m> les routers locaux du SDK sont réservés au dev client
17:40 < jrand0m> lol
17:40 < jrand0m> ok, comme je disais... ;)
17:40 < hezekiah> ;-)
17:41 < jrand0m> - nous avons besoin de quelqu'un pour commencer à travailler 	 sur une petite page web pour I2P qui servira à publier les différentes spécifications liées à I2P pour 	 relecture par les pairs.
17:41 < jrand0m> J'aimerais que ce soit prêt avant le 1/9.
17:41 < hezekiah> OK. Je dis tout de suite que vous ne voulez pas que ce soit moi qui fasse ça.
17:41 < hezekiah> Je ne suis pas un bon designer de pages web. :)
17:41 < jrand0m> moi non plus, si quelqu'un ici a vu mon flog ;)
17:41 < jrand0m> cohesion?  ;)
17:41 < hezekiah> lol
17:42 < hezekiah> Pauvre cohesion, toujours coincé avec les basses besognes. :-)
17:42  * cohesion lit le backlog
17:42 < hezekiah> ;)
17:42 < jrand0m> heh
17:42 < cohesion> jrand0m: Je vais le faire
17:42 < cohesion> me@jasonclinton.com
17:42 < cohesion> envoie-moi les specs
17:42 < jrand0m> 'k, gracias.
17:42 < jrand0m> les specs ne sont pas toutes finies.
17:43 < jrand0m> mais le contenu qui devra s'y trouver est :
17:43 < cohesion> eh bien, ce que tu as et ce que tu voudrais voir mis en ligne
17:43 < jrand0m> - spécification I2CP, spécification I2NP, spécification Polling HTTP 	 Transport, spécification TCP Transport, analyse de sécurité, analyse de performance, spécification des structures de données, 	 et un readme/intro
17:44 < jrand0m> (ces 7 documents seront en format PDF et/ou texte)
17:44 < cohesion> k
17:44 < jrand0m> sauf le readme/intro
17:45 < jrand0m> J'espère que tous ces docs seront prêts pour la semaine prochaine 	 (8/26).  ça te laissera assez de temps pour monter une petite page pour une sortie le 1/9 ?
17:46 < jrand0m> ok.  autre chose qui devra arriver, c'est 	 un simulateur de réseau I2P.
17:46 < jrand0m> on a quelqu'un qui cherche un projet d'info?  ;)
17:46 < hezekiah> lol
17:46 < cohesion> jrand0m: ouais, c'est faisable
17:47 < hezekiah> pas moi avant quelques années. ;-)
17:47 < jrand0m> cool cohesion
17:47 < thecrypto> pas avant un an
17:47  * cohesion retourne bosser
17:47 < jrand0m> merci cohesion
17:48 < jrand0m> ok, 1.6) prochaines deux semaines.  à mon agenda: mettre en ligne ces specs, 	 docs et analyses.  Je publierai &amp; committerai dès que possible.
17:48 < jrand0m> MERCI DE LIRE LES SPECS ET DE COMMENTER
17:48 < jrand0m> :)
17:48 < hezekiah> jrand0m: D'accord. Dès que j'aurai du temps, je commencerai à lire. :)
17:48 < jrand0m> Je préférerais que les gens postent les commentaires sur la liste, mais si 	 certains veulent être anon, envoyez-moi vos commentaires en privé et je posterai des réponses à 	 la liste anonymement.
17:49 < hezekiah> (Quelle est l'ETA pour que les 	 fichiers OpenOffice des docs soient sur CVS ?)
17:49 < jrand0m> Je peux committer les dernières revs dans les 10 minutes après 	 la fin de cette réunion.
17:49 < hezekiah> Génial. :)
17:50 < jrand0m> ok, c'est tout pour 1.*.
17:50 < jrand0m> 2.x) commentaires/questions/préoccupations/coups de gueule ?
17:50 < jrand0m> comment se passe la mod du SDK, mihi ?
17:51 < jrand0m> ou quelqu'un d'autre?  :)
17:51 < hezekiah> jrand0m: C'est quoi cette mod du SDK dont tu parles ?
17:52 < jrand0m> hezekiah> deux corrections de bug pour le SDK, commit (&amp; postées) 	 l'autre jour
17:52 < hezekiah> Ah
17:52 < hezekiah> Chouette.
17:52 < jrand0m> (faire tourner les IDs de message, synchroniser les écritures)
17:52 < hezekiah> Juste côté Java, ou aussi côté Python ?
17:52 < jrand0m> yo no hablo python.
17:53 < hezekiah> lol
17:53 < jrand0m> pas sûr que les bugs existent là.  est-ce que tu fais tourner les 	 message ids tous les 255 messages, et est-ce que tu synchronises tes écritures ?
17:54 < hezekiah> Je pense que le router Python fait les deux
17:54 < jrand0m> cool.
17:54 < jrand0m> on te dira si ce n'est pas le cas ;)
17:54 < hezekiah> Qu'entends-tu exactement par « synchronize your writes » ?
17:55 < jrand0m> aka s'assurer que plusieurs messages ne sont pas écrits à un client 	 en même temps s'il y a plusieurs clients qui essaient de lui envoyer des messages 	 en même temps.
17:55 < hezekiah> Toutes les données envoyées sur la connexion TCP sont envoyées 	 dans l'ordre où elles ont été produites.
17:56 < hezekiah> Donc tu n'auras pas 1/2 du message A puis 1/3 du message B.
17:56 < jrand0m> 'k
17:56 < hezekiah> Tu recevras le message A puis le message B.
17:56 < hezekiah> OK ... si personne d'autre ne parle, je propose que nous 	 levions la séance.
17:56 < mihi> mon simple TCP/IP au-dessus d'I2p semble fonctionner...
17:56 < jrand0m> niiiiice!!
17:56  * mihi était un peu en idle, désolé
17:57 < hezekiah> Quelqu'un d'autre a quelque chose à dire ?
17:57 < jrand0m> mihi> donc on pourra faire tourner pserver là-dessus ?
17:57 < mihi> tant que vous n'essayez pas de créer beaucoup de connexions d'un coup.
17:57 < mihi> jrand0m: je suppose - j'ai pu atteindre Google via ça
17:57 < jrand0m> niiiice
17:57 < jrand0m> mihi++
17:57 < mihi> jrand0m-ava
17:57 < jrand0m> donc tu as un outproxy et un inproxy ?
17:58 < mihi> exactement.
17:58 < jrand0m> cool
17:58 < mihi> la destination a besoin de clés, la source les génère à la demande
17:58  * hezekiah tend à jrand0m le *baf*er. Défonce le truc quand t'as 	 fini, mec.
17:58 < jrand0m> oui.  avec un peu de chance, le service de noms de co pourra aider avec ça 	 une fois prêt.
17:59 < jrand0m> ok cool.  mihi, dis-moi (ou à quelqu'un d'autre) s'il y a 	 quoi que ce soit qu'on puisse faire pour aider :)
17:59 < mihi> corrigez ce truc avec les 128 msgids ou construisez un meilleur support 	 GUARANTEED
17:59  * jrand0m assène un *baf* sur la tête de nop_afk parce qu'il a un vrai boulot
18:00 < mihi> jrand0m: l'abus du baf coûte 20 yodels
18:00 < jrand0m> lol
18:00 < jrand0m> un meilleur support garanti ?
18:00 < jrand0m> (aka de meilleures perfs que celles décrites?  on corrigera 	 ça dans l'impl)
18:00 < mihi> as-tu testé mon cas de test avec start_thread=end_thread=300?
18:01 < mihi> ça génère beaucoup de messages dans un sens, et ça fait que 	 tous les msgids sont engloutis...
18:01 < jrand0m> hmm, non, je n'avais pas vu ce message
18:01 < hezekiah> jrand0m: Ce serait raisonnable de faire des msgid sur 2 octets ?
18:01  * jrand0m a essayé les 200 / 201, mais c'est corrigé avec la dernière
18:01 -!- cohesion [cohesion@anon.iip] a quitté [off to the lug meeting]
18:01 < mihi> laquelle, la dernière ?
18:01 < hezekiah> Alors ils auraient 65535 msgids (si vous ne comptez 	 pas le msgid 0)
18:01 < hezekiah> .
18:02 < jrand0m> des message ids sur 2 octets ne feraient pas de mal.  Je suis 	 à l'aise avec ce changement.
18:02 < jrand0m> mihi> celle que je t'ai envoyée par mail
18:02 < mihi> si tu en as une plus récente que celle que tu m'as envoyée, envoie-la 	 (ou donne-moi un accès CVS)
18:03 < mihi> hmm, celle-là échoue chez moi avec 200/201 (ainsi qu'avec 300)
18:03 < jrand0m> hmm.  je vais faire plus de tests et de débogage et t'envoyer 	 par mail ce que je trouve.
18:03 < mihi> thx.
18:04 < jrand0m> ok.
18:04  * jrand0m déclare la réunion
18:04 < jrand0m> *baf*'ed
18:04  * hezekiah accroche le *baf*er avec révérence sur son râtelier spécial.
18:05  * hezekiah puis se retourne, sort par la porte en la claquant derrière 	 lui. Le baffer tombe du râtelier.
18:05 < hezekiah> ;-)
--- Journal fermé Tue Aug 19 18:05:36 2003 </div>
