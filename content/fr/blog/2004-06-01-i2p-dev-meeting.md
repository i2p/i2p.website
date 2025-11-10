---
title: "Réunion des développeurs d'I2P - 01 juin 2004"
date: 2004-06-01
author: "duck"
description: "Compte rendu de la réunion de développement d'I2P du 1er juin 2004."
categories: ["meeting"]
---

## Récapitulatif rapide

<p class="attendees-inline"><strong>Présents:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Journal de réunion

<div class="irc-log"> [22:59] &lt;duck&gt; mar. 1 juin 2004 21:00:00 UTC [23:00] &lt;duck&gt; salut tout le monde ! [23:00] &lt;mihi&gt; salut duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; ma proposition : [23:00] * Masterboy a rejoint #i2p

[23:00] <duck> 1) avancement du code
[23:00] <duck> 2) contenu à la une
[23:00] <duck> 3) état du réseau de test
[23:00] <duck> 4) primes
[23:00] <duck> 5) ???
[23:00] <Masterboy> salut:)
[23:00] <duck> .
[23:01] <duck> puisque jrandom est absent nous allons devoir le faire nous-mêmes
[23:01] <duck> (je sais qu'il journalise et vérifie notre indépendance)
[23:01] <Masterboy> pas de problème:P
[23:02] <duck> à moins qu'il y ait des problèmes avec l'ordre du jour je propose qu'on s'y tienne
[23:02] <duck> même si je ne peux pas faire grand-chose si vous ne le faites pas :)
[23:02] <duck> .
[23:02] <mihi> ;)
[23:02] <duck> 1) avancement du code
[23:02] <duck> pas beaucoup de code soumis à cvs
[23:02] <duck> j'ai remporté le trophée cette semaine: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus n'a pas encore de compte cvs
[23:03] <Masterboy> et qui a soumis quelque chose ?
[23:03] <duck> quelqu'un code-t-il secrètement ?
[23:03] * Nightblade a rejoint #I2P

[23:03] <hypercubus> BrianR travaillait sur des trucs
[23:04] <hypercubus> j'ai bricolé peut-être 20 % de l'installateur 0.4
[23:04] <duck> hypercubus: si tu as des trucs alors fournis des diffs et $dev fera le commit pour toi
[23:04] <duck> bien sûr les accords de licence stricts s'appliquent
[23:05] <duck> hypercubus: cool, des problèmes / choses à mentionner ?
[23:06] <hypercubus> pas encore, mais j'aurai probablement besoin de quelques utilisateurs BSD pour tester les scripts shell du pré-installateur
[23:06] * duck retourne quelques pierres
[23:06] <Nightblade> c'est uniquement en texte
[23:07] <mihi> duck: lequel es-tu sur duck_trophy.jpg ?
[23:07] <mihi> ;)
[23:07] <Nightblade> luckypunk a freebsd, mon FAI a aussi freebsd mais leur config est un peu bancale
[23:07] <Nightblade> mon FAI d'hébergement web, pas comcast
[23:08] <duck> mihi: celui de gauche avec les lunettes. wilde est le type à droite qui me remet le trophée
[23:08] * wilde fait coucou
[23:08] <hypercubus> tu as le choix... si tu as Java installé, tu peux ignorer complètement le pré-installateur...    si tu n'as pas Java installé tu peux lancer le pré-installateur binaire linux ou win32 (mode console), ou un    pré-installateur générique sous forme de script *nix (mode console)
[23:08] <hypercubus> le programme d'installation principal te donne le choix entre le mode console ou un mode GUI (interface graphique) sympa
[23:08] <Masterboy> je vais installer freebsd bientôt donc à l'avenir j'essaierai aussi l'installateur
[23:09] <hypercubus> ok bien... je ne savais pas si quelqu'un d'autre que jrandom l'utilisait
[23:09] <Nightblade> sur freebsd, Java est invoqué comme "javavm" plutôt que "java"
[23:09] <hypercubus> tel que construit à partir des sources sun ?
[23:09] <mihi> freebsd gère les liens symboliques ;)
[23:10] <hypercubus> en tout cas le pré-installateur binaire est complet à 100 %
[23:10] <hypercubus> compile avec gcj en natif
[23:11] <hypercubus> il te demande juste le répertoire d'installation et il récupère un JRE pour toi
[23:11] <duck> w00t
[23:11] <Nightblade> cool
[23:11] <hypercubus> jrandom prépare un JRE personnalisé pour i2p

[23:12] <deer> <j> .
[23:12] <Nightblade> si tu installes java depuis la collection de ports freebsd tu utilises un script wrapper appelé    javavm
[23:12] <deer> <r> .
[23:12] <hypercubus> bref, ce petit truc sera presque complètement automatisé
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <duck> r: coupe
[23:12] <deer> <r> .
[23:12] <deer> <m> .
[23:13] <deer> <m> serveur irc stupide, ne prend pas en charge le pipelining :(
[23:13] <duck> hypercubus: tu as un ETA pour nous ?
[23:14] <deer> <m> oups, le problème est "Changement de pseudo trop rapide" :(
[23:14] <hypercubus> je pense toujours terminer en moins d'un mois, avant que la 0.4 soit mûre pour une sortie
[23:14] <hypercubus> mais en ce moment je compile un nouvel OS pour mon système de dev, donc il faudra quelques jours    avant que je revienne sur l'installeur ;-)
[23:14] <hypercubus> pas d'inquiétude cependant
[23:15] <duck> ok. donc plus de nouvelles la semaine prochaine :)
[23:15] <duck> d'autres développements faits ?
[23:15] <hypercubus> je l'espère... à moins que la compagnie d'électricité ne me plante encore
[23:16] * duck se déplace vers #2
[23:16] <duck> * 2) contenu à la une
[23:16] <duck> beaucoup de streaming audio (ogg/vorbis) fait cette semaine
[23:16] <duck> baffled fait tourner son flux egoplay et moi je fais tourner un flux aussi
[23:16] <Masterboy> et ça marche plutôt bien
[23:17] <duck> sur notre site vous pouvez obtenir des infos sur comment l'utiliser
[23:17] <hypercubus> tu as des stats approximatives pour nous ?
[23:17] <duck> si vous utilisez un lecteur qui n'y est pas listé et que vous trouvez comment l'utiliser, merci de me les envoyer et je les    ajouterai
[23:17] <Masterboy> duck où est le lien vers le flux de baffled sur ton site ?
[23:17] <Masterboy> :P
[23:17] <duck> hypercubus: 4kB/s ça va plutôt bien
[23:18] <duck> et avec ogg c'est pas troooop mal
[23:18] <hypercubus> mais ça semble toujours être la vitesse moy. ?
[23:18] <duck> mon observation c'est que c'est le max
[23:18] <duck> mais c'est surtout du réglage de config
[23:19] <hypercubus> une idée pourquoi ça semble être le max ?
[23:19] <hypercubus> et je ne parle pas seulement de streaming ici
[23:19] <hypercubus> mais des téléchargements aussi
[23:20] <Nightblade> je téléchargeais de gros fichiers hier (quelques mégaoctets) depuis le service d'hébergement de duck    et j'obtenais environ 4kb-5kb aussi
[23:20] <duck> je pense que c'est le rtt
[23:20] <Nightblade> ces films Chips
[23:20] <hypercubus> 4-5 semble une amélioration par rapport aux ~3 que j'ai obtenus régulièrement depuis que j'ai commencé à utiliser i2p

[23:20] &lt;Masterboy&gt; 4-5kb ce n'est pas mal..
[23:20] &lt;duck&gt; avec un windowsize de 1 tu ne vas pas beaucoup plus vite..
[23:20] &lt;duck&gt; prime pour windowsize&gt;1 : http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi : tu peux commenter ?
[23:21] &lt;hypercubus&gt; mais c'est un 3 kbps remarquablement constant
[23:21] &lt;mihi&gt; sur quoi ? windowsize>1 avec ministreaming : tu es un magicien si tu y arrives ;)
[23:21] &lt;hypercubus&gt; aucun à-coup sur le compteur de bande passante... une ligne assez régulière
[23:21] &lt;duck&gt; mihi : sur la raison pour laquelle c'est si stable à 4kb/s
[23:21] &lt;mihi&gt; aucune idée. je n'entends aucun son :(
[23:22] &lt;duck&gt; mihi : pour tous les transferts i2ptunnel
[23:22] &lt;Masterboy&gt; mihi tu dois configurer le plugin de streaming Ogg..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; non, il n'y a aucune limite à l'intérieur de i2ptunnel concernant la vitesse. ça doit être dans le router...
[23:23] &lt;duck&gt; mon raisonnement : taille max de paquet : 32kB, rtt de 5 secondes : 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; ça paraît plausible
[23:25] &lt;duck&gt; ok..
[23:25] &lt;duck&gt; autre contenu :
[23:25] * hirvox a rejoint #i2p

[23:25] &lt;duck&gt; il y a un nouvel eepsite de Naughtious
[23:25] &lt;duck&gt; anonynanny.i2p
[23:25] &lt;duck&gt; la clé a été committée dans CVS et il l’a mise sur le wiki d’ugha
[23:25] * mihi entend « sitting in the ... » - duck++
[23:25] &lt;Nightblade&gt; vois si tu peux ouvrir deux ou trois flux à 4kb, alors tu pourras dire si c’est dans le router ou dans la bibliothèque de streaming
[23:26] &lt;duck&gt; Naughtious : tu es là ? dis-nous quelque chose sur ton plan :)
[23:26] &lt;Masterboy&gt; j’ai lu qu’il propose de l’hébergement
[23:26] &lt;duck&gt; Nightblade : j’ai essayé 3 téléchargements parallèles depuis baffled et j’avais 3-4kB chacun
[23:26] &lt;Nightblade&gt; je vois
[23:27] &lt;mihi&gt; Nightblade : comment peux-tu l’affirmer alors ?
[23:27] * mihi aime écouter en mode « stop&go » ;)
[23:27] &lt;Nightblade&gt; eh bien s’il y a une sorte de limitation dans le router qui ne lui permet de gérer que 4kb à la fois
[23:27] &lt;Nightblade&gt; ou si c’est autre chose
[23:28] &lt;hypercubus&gt; quelqu’un peut expliquer ce site anonynanny ? je n’ai pas d’i2p router en marche pour le moment
[23:28] &lt;mihi&gt; hypercubus : juste un wiki ou quelque chose du genre
[23:28] &lt;duck&gt; un Plone CMS, création de compte ouverte
[23:28] &lt;duck&gt; permet l’envoi de fichiers et des trucs de site web
[23:28] &lt;duck&gt; via l’interface web
[23:28] &lt;Nightblade&gt; une autre chose à faire serait de tester le débit du « repliable datagram » (datagramme auquel on peut répondre) qui, à ce que je sache, est le même que les flux mais sans acks (accusés de réception)
[23:28] &lt;duck&gt; probablement très proche de Drupal
[23:28] &lt;hypercubus&gt; ouais, j’ai déjà fait tourner Plone
[23:29] &lt;duck&gt; Nightblade : je pensais utiliser airhook pour gérer ça
[23:29] &lt;duck&gt; mais pour l’instant ce ne sont que des idées de base
[23:29] &lt;hypercubus&gt; tout est permis pour le contenu du wiki, ou ça se concentre sur quelque chose en particulier ?
[23:29] &lt;Nightblade&gt; je crois qu’airhook est sous licence GPL
[23:29] &lt;duck&gt; le protocole
[23:29] &lt;duck&gt; pas le code
[23:29] &lt;Nightblade&gt; ah :)
[23:30] &lt;duck&gt; hypercubus : il veut du contenu de qualité, et il te laisse le fournir :)
[23:30] &lt;Masterboy&gt; mets en ligne le meilleur pr0n de toi que tu as, hyper ;P
[23:30] &lt;duck&gt; ok
[23:30] * Masterboy essaiera de faire ça aussi
[23:30] &lt;hypercubus&gt; ouais, quiconque ouvre un wiki réclame forcément du contenu de qualité ;-)
[23:31] &lt;duck&gt; ok
[23:31] * duck passe au point n°3
[23:31] &lt;duck&gt; * 3) état du réseau de test (testnet)
[23:31] &lt;Nightblade&gt; Airhook gère élégamment les réseaux intermittents, peu fiables ou retardés  &lt;-- héhé pas une description très optimiste d’I2P !
[23:31] &lt;duck&gt; comment ça se passe ?
[23:32] &lt;duck&gt; mettons la discussion sur les datagrammes sur i2p à la fin
[23:32] &lt;tessier&gt; j’adore courir sur les wikis ouverts et lier vers ceci : http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] &lt;tessier&gt; airhook déchire
[23:32] &lt;tessier&gt; je l’ai étudié aussi pour construire un réseau p2p.
[23:32] &lt;Nightblade&gt; ça me paraît fiable (#3)
[23:32] &lt;Nightblade&gt; le meilleur que j’aie vu jusqu’ici
[23:33] &lt;duck&gt; ouais
[23:33] &lt;mihi&gt; ça marche bien — au moins pour l’audio en streaming « stop&go »
[23:33] &lt;duck&gt; je vois des uptimes assez impressionnants sur IRC
[23:33] &lt;hypercubus&gt; d’accord… je vois beaucoup plus de bonshommes bleus dans ma console du router
[23:33] &lt;Nightblade&gt; mihi : tu écoutes de la techno ? :)
[23:33] &lt;duck&gt; mais difficile à dire puisque bogobot ne semble pas gérer les connexions qui passent 00:00
[23:33] &lt;tessier&gt; le streaming audio marche super chez moi mais charger des sites web demande souvent plusieurs essais
[23:33] &lt;Masterboy&gt; j’ai l’impression qu’i2p tourne très bien après 6 heures d’utilisation ; à la 6e heure j’ai utilisé l’IRC pendant 7 heures et donc mon router tournait depuis 13 heures
[23:33] &lt;duck&gt; (*indice*)
[23:34] &lt;hypercubus&gt; duck : euh… héhé
[23:34] &lt;hypercubus&gt; je pourrais corriger ça je suppose
[23:34] &lt;hypercubus&gt; tu as la journalisation réglée en quotidien ?
[23:34] &lt;duck&gt; hypercubus++
[23:34] &lt;hypercubus&gt; je veux dire la rotation des logs
[23:34] &lt;duck&gt; oh oui
[23:34] &lt;duck&gt; duck--
[23:34] &lt;hypercubus&gt; c’est pour ça
[23:34] &lt;Nightblade&gt; j’étais au travail toute la journée, j’ai allumé mon ordinateur, démarré i2p et j’étais sur le serveur IRC de duck en quelques minutes
[23:35] &lt;duck&gt; j’ai vu des DNF bizarres
[23:35] &lt;duck&gt; même en me connectant à mes propres eepsites
[23:35] &lt;duck&gt; (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] &lt;duck&gt; je pense que c’est ce qui cause la plupart des problèmes maintenant
[23:35] &lt;hypercubus&gt; bogoparser n’analysera que les uptimes entièrement contenus dans un seul fichier de log… donc si le fichier de log ne couvre que 24 heures, personne n’apparaîtra connecté plus de 24 heures
[23:35] &lt;duck&gt; Masterboy et ughabugha l’ont eu aussi je crois…
[23:36] &lt;Masterboy&gt; ouais
[23:36] &lt;duck&gt; (corrige ça et tu gagneras le trophée de la semaine prochaine à coup sûr !)
[23:37] &lt;deer&gt; &lt;mihi&gt; bogobot est excité ? ;)
[23:37] &lt;Masterboy&gt; j’ai essayé mon site web et parfois quand j’appuie sur actualiser il prend un autre chemin ? et je dois attendre que ça charge mais je n’attends jamais ;P je ré-appuie et ça s’affiche instantanément
[23:37] &lt;deer&gt; &lt;mihi&gt; oups, désolé. j’avais oublié que c’est relayé…
[23:38] &lt;duck&gt; Masterboy : les timeouts durent 61 secondes ?
[23:39] &lt;duck&gt; mihi : bogobot est réglé en rotation hebdomadaire maintenant
[23:39] * mihi a quitté IRC (« bye, et bonne réunion »)
[23:40] &lt;Masterboy&gt; désolé, je n’ai pas vérifié ; sur mon site quand je ne peux pas l’atteindre instantanément je fais juste actualiser et ça charge instantanément..
[23:40] &lt;duck&gt; hm
[23:40] &lt;duck&gt; bon, il faut corriger ça
[23:41] &lt;duck&gt; .... #4
[23:41] &lt;Masterboy&gt; je pense que le chemin n’est pas le même à chaque fois
[23:41] &lt;duck&gt; * 4) primes (bounties)
[23:41] &lt;duck&gt; Masterboy : les connexions locales devraient être raccourcies
[23:42] &lt;duck&gt; wilde avait quelques idées de primes… tu es là ?
[23:42] &lt;Masterboy&gt; peut-être que c’est un bug de sélection de pairs
[23:42] &lt;wilde&gt; je ne suis pas sûr que ça devait vraiment être à l’ordre du jour
[23:42] &lt;duck&gt; oh
[23:42] &lt;wilde&gt; ok mais les idées étaient quelque chose comme :
[23:42] &lt;Masterboy&gt; je pense que quand on ira public, le système de primes fonctionnera mieux
[23:43] &lt;Nightblade&gt; masterboy : oui, il y a deux tunnels pour chaque connexion, du moins c’est comme ça que je le comprends en lisant le router.config
[23:43] &lt;wilde&gt; on pourrait profiter de ce mois pour faire un peu de pub pour i2p et augmenter un peu la cagnotte des primes
[23:43] &lt;Masterboy&gt; je vois que le projet Mute se porte bien — ils ont eu 600$ et ils n’ont pas encore beaucoup codé ;P
[23:44] &lt;wilde&gt; cibler les communautés de la liberté, les gens de la crypto, etc.
[23:44] &lt;Nightblade&gt; je ne crois pas que jrandom veuille de la publicité
[23:44] &lt;wilde&gt; pas l’attention publique de Slashdot, non
[23:44] &lt;hypercubus&gt; c’est ce que j’ai observé aussi
[23:44] &lt;Masterboy&gt; je veux relancer ça — quand on ira public le système fonctionnera bien mieux ;P
[23:45] &lt;wilde&gt; Masterboy : les primes pourraient accélérer le développement de myi2p par exemple
[23:45] &lt;Masterboy&gt; et comme jr l’a dit, pas de public avant la 1.0 et seulement un peu d’attention après 0.4
[23:45] &lt;Masterboy&gt; *a écrit
[23:45] &lt;wilde&gt; quand on aura genre $500+ pour une prime, des gens pourraient réellement tenir quelques semaines
[23:46] &lt;hypercubus&gt; le délicat, c’est que même si on vise une petite communauté de dev, genre *toussote* les devs de Mute, ces gars pourraient parler d’i2p plus largement que nous ne le voudrions
[23:46] &lt;Nightblade&gt; quelqu’un pourrait faire carrière en corrigeant des bugs i2p
[23:46] &lt;hypercubus&gt; et trop tôt
[23:46] &lt;wilde&gt; des liens i2p sont déjà à beaucoup d’endroits publics
[23:46] &lt;Masterboy&gt; tu cherches sur Google et tu peux trouver i2p

[23:47] &lt;hypercubus&gt; des endroits publics obscurs ;-) (j'ai vu le lien I2P sur un freesite (site publié sur Freenet)... j'ai de la chance que ce fichu freesite    ait même chargé !) [23:47] &lt;wilde&gt; http://en.wikipedia.org/wiki/I2p [23:47] &lt;Masterboy&gt; mais je suis d'accord: pas de publicité jusqu'à ce que la 0.4 soit terminée [23:47] &lt;Masterboy&gt; quoi??????? [23:47] &lt;wilde&gt; http://www.ovmj.org/GNUnet/links.php3?xlang=English [23:48] &lt;Masterboy&gt; protol0l fait du super boulot ;P [23:48] &lt;Masterboy&gt; ;)))))) [23:48] &lt;hypercubus&gt; jolie faute de frappe ;-) [23:48] &lt;wilde&gt; ok de toute façon, je suis d'accord qu'on devrait encore garder I2P privé (jr lis ce log ;) [23:49] &lt;Masterboy&gt; qui a fait ça ? [23:49] &lt;Masterboy&gt; je pense que la discussion de l'équipe Freenet a attiré plus d'attention.. [23:50] &lt;Masterboy&gt; et jr qui discute avec toad donne beaucoup d'infos au grand public.. [23:50] &lt;Masterboy&gt; donc comme dans ughas wiki - on peut tous blâmer jr pour ça ;P [23:50] &lt;wilde&gt; ok de toute façon, on va voir si on peut faire entrer un peu de $ sans attirer /. [23:50] &lt;Masterboy&gt; d'accord [23:50] &lt;hypercubus&gt; la liste des dévs Freenet, c'est difficilement ce que j'appelle le « grand public » ;-) [23:50] &lt;wilde&gt; . [23:51] &lt;hypercubus&gt; wilde : tu auras beaucoup de $ plus tôt que tu ne le penses ;-) [23:51] &lt;wilde&gt; oh allez, même ma mère est abonnée à freenet-devl [23:51] &lt;duck&gt; ma mère lit via gmame [23:51] &lt;deer&gt; &lt;clayboy&gt; freenet-devl est enseignée dans les écoles ici [23:52] &lt;wilde&gt; . [23:52] &lt;Masterboy&gt; donc on verra plus de primes après le passage en 0.4 stable.. [23:53] &lt;Masterboy&gt; c'est dans 2 mois ;P [23:53] &lt;wilde&gt; où est passé ce duck ? [23:53] &lt;duck&gt; merci wilde   [23:53] &lt;hypercubus&gt; même si, en tant que seul demandeur de prime jusqu'à présent, je dois dire que l'argent de la prime n'a eu aucune    influence sur ma décision de relever le défi [23:54] &lt;wilde&gt; héhé, ça l'aurait fait si ça avait été 100x [23:54] &lt;duck&gt; tu es trop bon pour le monde [23:54] &lt;Nightblade&gt; haha [23:54] * duck se déplace vers #5 [23:54] &lt;hypercubus&gt; wilde, 100 $ ça ne représente rien pour moi ;-) [23:54] &lt;duck&gt; 100 * 10 = 1000 [23:55] * duck pops("5 airhook") [23:55] &lt;duck&gt; tessier : tu as une expérience concrète avec ça [23:55] &lt;duck&gt; (http://www.airhook.org/) [23:55] * Masterboy va essayer ça:P [23:56] &lt;duck&gt; implémentation Java (je ne sais même pas si ça marche) http://cvs.ofb.net/airhook-j/ [23:56] &lt;duck&gt; implémentation Python (un bazar, a fonctionné par le passé) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py [23:58] * duck ouvre la vanne à râler [23:58] &lt;Nightblade&gt; celle en j est aussi gpl [23:58] &lt;duck&gt; passez-la dans le domaine public [23:58] &lt;hypercubus&gt; amen [23:58] &lt;Nightblade&gt; toute la doc du protocole fait à peine 3 pages - ça ne peut pas être si difficile [23:59] &lt;Masterboy&gt; rien n'est difficile [23:59] &lt;Masterboy&gt; c'est juste pas facile [23:59] &lt;duck&gt; je ne pense pas que ce soit entièrement spécifié pour autant [23:59] * hypercubus confisque les biscuits chinois de masterboy [23:59] &lt;duck&gt; il faudra peut-être plonger dans le code C pour une implémentation de référence [00:00] &lt;Nightblade&gt; je le ferais moi-même mais je suis occupé avec d'autres trucs i2p en ce moment [00:00] &lt;Nightblade&gt; (et aussi mon travail à plein temps) [00:00] &lt;hypercubus&gt; duck : peut-être une prime pour ça ? [00:00] &lt;Nightblade&gt; il y en a déjà une [00:00] &lt;Masterboy&gt; ? [00:00] &lt;Masterboy&gt; ahh Pseudonyms [00:00] &lt;duck&gt; ça pourrait être utilisé à 2 niveaux [00:00] &lt;duck&gt; 1) comme transport en plus de TCP [00:01] &lt;duck&gt; 2) comme protocole pour gérer des datagrammes à l'intérieur de i2cp/sam [00:01] &lt;hypercubus&gt; ça mérite une sérieuse considération alors [00:01] &lt;hypercubus&gt; &lt;/obvious&gt;

[00:02] &lt;Nightblade&gt; duck: j’ai remarqué que le datagramme répliable dans SAM a une taille maximale de 31 Ko, tandis que le    stream (flux) a une taille maximale de 32 Ko - ce qui me fait penser que la destination de l’expéditeur est envoyée avec chaque paquet en    mode datagramme répliable, et seulement au début pour un mode stream -
[00:02] &lt;Masterboy&gt; eh bien airhook cvs n’est pas très à jour..
[00:03] &lt;Nightblade&gt; ce qui me fait penser qu’il serait inefficace de construire un protocole au-dessus des    datagrammes répliables via SAM
[00:03] &lt;duck&gt; la taille de message d’airhook est de 256 octets, celle d’i2cp est de 32 Ko, donc il faut au moins changer un peu
[00:04] &lt;Nightblade&gt; en fait, si tu voulais faire le protocole dans SAM, tu pourrais simplement utiliser le datagramme anonyme    et faire en sorte que le premier paquet contienne la destination de l’expéditeur.... blablabla - j’ai plein d’idées mais pas    assez de temps pour les coder
[00:06] &lt;duck&gt; mais encore, tu as des problèmes pour vérifier les signatures
[00:06] &lt;duck&gt; donc quelqu’un pourrait t’envoyer de faux paquets
[00:06] &lt;Masterboy&gt; sujet:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; vrai
[00:08] &lt;Nightblade&gt; mais si tu renvoyais vers cette destination et qu’il n’y avait pas d’accusé de réception, tu saurais que c’était    un imposteur
[00:08] &lt;Nightblade&gt; il faudrait un handshake (échange d’initialisation)
[00:08] &lt;duck&gt; mais il te faudra des handshakes au niveau applicatif pour ça
[00:08] &lt;Nightblade&gt; non, pas vraiment
[00:09] &lt;Nightblade&gt; il suffit de le mettre dans une bibliothèque pour accéder à SAM
[00:09] &lt;Nightblade&gt; c’est une mauvaise façon de faire, cela dit
[00:09] &lt;Nightblade&gt; de le faire pourtant
[00:09] &lt;duck&gt; tu pourrais aussi utiliser des tunnels séparés
[00:09] &lt;Nightblade&gt; ça devrait être dans la bibliothèque de streaming
[00:11] &lt;duck&gt; oui. ça se tient
[00:12] &lt;duck&gt; ok
[00:12] &lt;duck&gt; je me sens d’humeur *baff*
[00:13] &lt;Nightblade&gt; ja
[00:13] * duck *baffs* </div>
