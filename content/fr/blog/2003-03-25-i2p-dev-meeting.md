---
title: "Réunion des développeurs d'I2P"
date: 2003-03-25
author: "nop"
description: "Réunion de développement d'I2P portant sur les mises à jour du projet et les discussions techniques"
categories: ["meeting"]
---

(Avec l'aimable autorisation de la Wayback Machine http://www.archive.org/)

## Récapitulatif rapide

<p class="attendees-inline"><strong>Présents:</strong> Aprogas, hezekiah, mids, mihi, nop, noP, UserX</p>

## Journal de réunion

<div class="irc-log"> --- Journal ouvert Tue Mar 25 22:07:19 2003
22:07 -!- Sujet pour #iip-dev: Réunion IIP - fichiers journaux: http://mids.student.utwente.nl/~mids/iip/
22:07 [Utilisateurs #iip-dev]
22:07 [@hezekiah] [ Aprogas] [ logger] [ mids] [ poX] [ UserX]
22:07 -!- Irssi: #iip-dev: Total de 6 pseudos [1 ops, 0 halfops, 0 voices, 5 normaux]
22:07 -!- Irssi: La connexion au #iip-dev a été synchronisée en 3 secondes
22:07 < UserX> oui
22:07 <@hezekiah> OK. :)
22:07 < mids> le journal est en ligne http://mids.student.utwente.nl/~mids/iip/meeting35/livelog.txt
22:07 < Aprogas> /exec -o tail -f http://mids.student.utwente.nl/~mids/iip/meeting35/livelog.txt
22:08 < Aprogas> les boucles sont amusantes
22:08 < mids> à moins que quelqu'un n'ait un ordre du jour ;
22:08 < mids> j'aimerais entendre quelles sont les propositions officielles pour le protocole de routage décentralisé
22:09 < Aprogas> alors mettons au moins  1. protocole de routage décentralisé 2. question  à l'ordre du jour
22:09 < mids> 1) bienvenue
22:09 < mids> 2) protocole décentralisé
22:09 < mids> 3) WVTTK
22:09 < mids> 4) questions
22:09 < Aprogas> c'est du néerlandais
22:10 < mids> quel est le mot anglais pour ça ?
22:10 < Aprogas> 3) WCTTA
22:10 < Aprogas> peut-être
22:10 < Aprogas> mais le latin serait plus élitiste
22:10 < Aprogas> où est le directeur pour me dire de la fermer et de revenir au sujet ?
22:10 <@hezekiah> Aprogas : tais-toi et reviens au sujet. ;-)
22:10 < mids> quod etcetera mensa venit
22:11 < Aprogas> hezekiah : merci
22:11 < mids> -1-
22:11 < mids> Bienvenue à tous !
22:11 <@hezekiah> Salut ! :)
22:11 < mids> comme vous le voyez, à partir de maintenant les réunions régulières auront lieu plus tôt que les 33 précédentes
22:11 < mihi> salut mids
22:11 < mids> .
22:11 < mids> -2-
22:11 < Aprogas> pour mieux convenir aux utilisateurs IIP principalement US/UE ?
22:12 < nop> yo
22:12 < Aprogas> salut nop
22:12 -!- mode/#iip-dev [+o nop] par Trent
22:12 <@nop> j'ai la page
22:12 <@hezekiah> Salut, nop ! :)
22:12 < mids> Aprogas : cela conviendrait mieux pour UserX / nop
22:12 <@nop> UserX est en vie ?
22:12 < Aprogas> n'oublie pas de changer ton pseudo en noP
22:12 -!- nop est maintenant connu sous le nom de noP
22:12 < mids> 2) j'aimerais entendre quelles sont les propositions officielles pour le protocole de routage décentralisé
22:12 <@noP> merci aprogas
22:12 <@noP> nous n'avons pas de proposition officielle avant vendredi 21:00
22:12 < UserX> noP : je suis là
22:13 <@noP> cela doit être discuté
22:13 <@noP> il y a des propositions semi-officielles sur www.invisiblenet.net/research
22:13 < Aprogas> puis-je rejoindre cette discussion pour donner des suggestions totalement inutiles ?
22:13 <@noP> qui sont de nombreuses propositions différentes
22:13 <@hezekiah> Euh, oh. On dirait que j'ai beaucoup de lecture à faire avant vendredi. ;-)
22:13 <@noP> nous l'enregistrerons
22:13 <@noP> et tu peux proposer
22:13 <@noP> pendant la réunion iip-dev
22:14 <@noP> oui hezekiah nous avons ajouté plus de choses ;)
22:14 -!- mids a changé le sujet de #iip-dev en : Réunion IIP - fichiers journaux : http://mids.student.utwente.nl/~mids/iip/ - http://www.invisiblenet.net/research/
22:14 < mids> ok
22:14 < mids> .
22:14 < mids> quod etcetera mensa venit?
22:14 <@noP> brb
22:14 <@hezekiah> mids : C'est quelle langue ?
22:15 < mids> latin
22:15 <@hezekiah> Ah.
22:15 < Aprogas> mensam semble plus correct
22:15 < mids> ça devrait vouloir dire quelque chose comme : quoi d'autre vient à la table
22:15 < Aprogas> et `etcetera' ne l'est pas
22:15 < mids> et cetera
22:15 < Aprogas> mais ça n'a toujours aucun sens
22:16 < mihi> quod ceterum ad mensam venit?
22:16 < Aprogas> peut-être
22:16 < Aprogas> quand le code source d'IIP sera-t-il traduit en latin en utilisant latin.h ?
22:16 < mihi> igpay atinlay? ;-)
22:16 < Aprogas> en d'autres termes, quand est-ce que le développement d'IIP sera gelé pour transférer ces heures-homme vers mon projet latin.h et le terminer, puis seulement l'implémenter dans IIP ?
22:17 <@hezekiah> Jamais.
22:17 < mids> quod autem ad mensam venit
22:17 < mids> propulsé par http://www.latijnnederlands.nl/
22:17 < mids> .
22:17 < Aprogas> c'est W Echter TTK
22:17 < mids> des questions sur IIP ?
22:17 < mids> Aprogas: 2. verder, voorts, en dan (ter voortzetting of uitwerking v. iets voorafgaands).
22:17 < mihi> "*but* what comes to the table"?
22:17 < Aprogas> `what' le fait
22:18 < mids> mihi : questions, propositions, commentaires
22:18 < mihi> mids, tu as oublié les ""
22:18 < Aprogas> tout ce dont on a parlé pendant la réunion mais qui n'entrait pas dans le point en cours
22:18 <@hezekiah> Est-ce le point 3 de l'ordre du jour ?
22:18 < Aprogas> hezekiah : je pense que nous en sommes déjà aux questions
22:18 < mids> hezekiah : oui
22:18 < Aprogas> la réunion semble chaotique et sans contenu réel, sauf que la décision sur le protocole de routage sera prise plus tard
22:18 <@hezekiah> … parce que je n'ai aucune idée de ce que signifie « WVTTK » et cette conversation est clairement assez obscure pour être une candidate possible. ;-)
22:19 < mids> ok, /me formalizes
22:19 <@hezekiah> Exact
22:19 < Aprogas> c'est probablement parce que je suis là
22:19 < mids> et parce que j'ai bu beaucoup de bière
22:19 < Aprogas> WVTTK en réalité est tout ce qui n'a pas de sens
22:19  * mids passe au point 4
22:20 < mids> des questions liées à IIP ?
22:20 < Aprogas> comment l'équipe IIP s'attend-elle à voir la base d'utilisateurs croître, et quand une campagne massive de RP commencera-t-elle pour stimuler davantage la croissance ?
22:20 < Aprogas> de plus, quel type de personnes l'équipe IIP s'attend-elle à attirer au début, et avec la campagne de RP
22:21 < mids> l'expérience passée a appris qu'il est très facile de passer sur slashdot
22:21 < mids> ce qui se traduit par une augmentation rapide des utilisateurs
22:21 < mids> mais il faut des Fonctionnalités Cool
22:21 < mids> pour justifier une annonce
22:21 < Aprogas> eh bien, la plupart des utilisateurs de slashdot ne restent pas longtemps je pense
22:21 < Aprogas> quelques-uns restent, mais la plupart veulent juste `check it out'
22:21 <@hezekiah> Exact.
22:21 <@hezekiah> Donc une fois que nous décentraliserons, nous aurons quelque chose à fanfaronner sur /.
22:22 < mids> ensuite nous pourrons contacter quelques magazines en ligne
22:22 < mids> comme theregister
22:22 < mids> et/ou wired
22:22 < Aprogas> il faut des fonctionnalités cool pour justifier une annonce, et il faut une application cool pour les retenir
22:22 <@hezekiah> Exact.
22:22 < Aprogas> mais slashdot est un groupe cible assez `limited'
22:22 < Aprogas> ça n'attire qu'un certain type de personnes
22:22 < mids> c'est une partie
22:22 < Aprogas> un peu plus de diversité serait peut-être bien
22:22 < mids> on pourrait aussi viser certains publics cibles
22:22 <@hezekiah> Personnellement, je me soucie peu d'attirer des gens. Je veux juste un bon programme.
22:23 < mids> comme écrire à l'organisation néerlandaise Martijn :)
22:24 < mids> peut-être un communiqué de presse aux groupes des AA, Amnesty, l'EFF, les critiques de la scientologie/des sectes
22:24 < mids> hezekiah : même avec un bon programme il faut une certaine base d'utilisateurs pour pouvoir offrir un trafic correct
22:25 < mids> tu ne peux pas n'avoir que 2 utilisateurs sur ton réseau ultra-anonyme
22:25 <@hezekiah> De mon point de vue, si c'est assez facile à trouver sur freashmeat/sourceforge et que ça offre ce que les gens veulent (un bon chat anonymisé), alors les gens l'utiliseront.
22:26 <@hezekiah> Oui. C'est une vision très primitive de la croissance de la base d'utilisateurs.
22:26 < Aprogas> l'internaute moyen ne cherche pas sur sourceforge
22:26 < Aprogas> il est difficile de chercher quelque chose si tu ne sais pas que ça existe
22:26 < mids> hezekiah : freshmeat / sourceforge c'est seulement pour les geeks
22:26 < mids> ils pensent que l'anonymat est 'cool'
22:26 < mids> mais n'en ont pas vraiment tant besoin
22:26 <@hezekiah> Ou ils ont des gens qu'ils ne veulent pas avoir derrière leur épaule. :)
22:26 < mids> car ils n'ont rien à cacher :)
22:27 <@hezekiah> Mais leur paranoïa les aide à mettre en place des nœuds sécurisés.
22:27 <@hezekiah> Je ne suis pas sûr de vouloir que mon trafic de messages passe par la machine Windows Me de Grande-Tante Edna.
22:27 < mids> quel est le public cible à ton avis ?
22:27 < mids> des gamins Linux de 16 à 23 ans ?
22:27 <@hezekiah> Eh bien, je me fiche vraiment de qui l'utilise.
22:28 < mids> ou monsieur Tout-le-monde
22:28 <@hezekiah> Je voudrais seulement que les gens qui montent les nœuds les fassent de manière sécurisée.
22:28 < Aprogas> peut-être quelques avocats pour nous défendre
22:28 <@hezekiah> Au-delà de ça, je veux juste améliorer le programme par un bon code.
22:28 < Aprogas> si IIP est un programme correct, il prendrait en compte que tous les nœuds ne peuvent pas être sécurisés
22:28 <@hezekiah> Nop fait des choses liées à la base d'utilisateurs. Il semble bien comprendre ça.
22:29 < mids> qu'entends-tu par là ?
22:29 < Aprogas> hezekiah est le vrai programmeur, il a peur des utilisateurs
22:29 <@hezekiah> Aprogas : IIP fera de son mieux pour être à l'épreuve des idiots, mais la sécurité d'un système dépend toujours des personnes qui le font fonctionner.
22:29 <@hezekiah> Aprogas : je n'ai pas peur des utilisateurs. Je me soucie juste assez peu de _qui_ ils sont.
22:29 < mids> http://www.joelonsoftware.com/articles/StrategyLetterV.html
22:30 <@hezekiah> mids : il fait des trucs corporate. Des choses de business. Je ne sais toujours pas comment il a obtenu des fonds pour embaucher Cap'n Crunch.
22:30 < mids> pas de commentaire
22:30 <@hezekiah> lol
22:33 < mids> je n'ai plus rien à dire
22:33 < mids> d'autres questions ?
22:33 < Aprogas> combien de développeurs IIP a-t-il en ce moment, et combien d'heures par semaine ces développeurs y consacrent-ils (estimé)
22:33 <@hezekiah> Euh ..
22:34 <@hezekiah> En fait, c'est une question piège. :)
22:34 < Aprogas> ah oui ?
22:34 <@hezekiah> Quel _type_ de développeurs cherches-tu ?
22:34 < Aprogas> je ne cherche pas de développeurs
22:34 < Aprogas> je veux juste savoir comment va le développement d'IIP
22:34 <@hezekiah> Donc tu veux savoir qui sont les développeurs qui écrivent isproxy ?
22:35 < Aprogas> IIP c'est plus que juste isproxy je suppose
22:35 <@hezekiah> Oui.
22:35 < Aprogas> je veux juste savoir combien de personnes passent actuellement du temps sur IIP
22:35 <@hezekiah> C'est pour ça que c'est une question piège. :)
22:35 <@hezekiah> Alors je n'en ai aucune idée ! :) Ils ne sont probablement pas tous publics !
22:35 < mids> combien de temps passes-tu sur IIP alors ?
22:35 < Aprogas> laisse tomber, je vais juste aller regarder le compteur d'activité de sf je suppose
22:36 < Aprogas> s'il a ce genre d'informations
22:36 <@hezekiah> Je peux te dire que pour l'instant (à ma connaissance) il n'y a vraiment que deux personnes qui écrivent activement du code pour la source isproxy.
22:36 <@hezekiah> UserX et moi.
22:36 < mids> *hoche la tête*
22:36 < Aprogas> je ne parle pas seulement d'écrire du code
22:36 <@hezekiah> Nop fait des trucs en arrière-plan quand il peut, qui touchent à de chouettes protocoles et à la théorie.
22:36 < Aprogas> aussi de la planification, par exemple ce protocole de routage
22:36 < Aprogas> juste le projet dans son ensemble
22:36 <@hezekiah> OK ... c'est un projet open source. Les « développeurs » sont tous ceux qui apportent une idée.
22:37 <@hezekiah> lol
22:37 < Aprogas> en fait je veux savoir combien d'heures-homme sont passées (gaspillées ?) sur IIP, pour pouvoir calculer combien d'argent cela représente
22:37 <@hezekiah> Beaucoup plus difficile à répondre que tu ne le pensais, hein ?
22:37 <@hezekiah> Eh bien, je ne connais à peu près que le travail sur isproxy.
22:37 < Aprogas> ok
22:37 <@hezekiah> Ça fluctue selon à quel point UserX et moi sommes occupés.
22:37 <@noP> aprogas tu chipotes
22:38 < Aprogas> c'est juste que je veux savoir que si je devais donner de l'argent à ce projet, j'en donne le bon montant, ni trop, ni trop peu
22:38 <@noP> si tu n'es pas dans l'équipe de dev
22:38 <@noP> alors ne perds tout simplement pas ton temps
22:38 <@hezekiah> Par exemple, en ce moment je suis très pris dans la vraie vie, donc je n'ai pas pu toucher au code isproxy depuis plus d'une semaine ! (Argh !)
22:38 < Aprogas> donc je veux savoir combien ce projet `coûterait' en heures-homme
22:39 <@hezekiah> Sur une semaine moyenne où je peux écrire du code, je peux faire 4-5 heures. C'est une estimation au doigt mouillé ! UserX semble coder par à-coups (sans offense), avec des périodes où il n'a pas beaucoup de temps puis une semaine avec une rafale de commits. (Il pourrait très bien coder tout le temps et ne faire des commits que quand il a du code terminé. Je ne sais pas vraiment.)
22:39 <@hezekiah> De toute façon, c'est bien trop volatile pour que je puisse vraiment l'estimer.
22:40 < Aprogas> ok
22:41 < Aprogas> je n'ai plus de questions
22:43  * mids met fin à la souffrance
22:43  * hezekiah tend à mids le *baf*er
22:44 -!- mode/#iip-dev [+o mids] par Trent
22:44 -!- logger a été expulsé de #iip-dev par mids [*baf*]
--- Journal fermé Tue Mar 25 22:45:02 2003 </div>
