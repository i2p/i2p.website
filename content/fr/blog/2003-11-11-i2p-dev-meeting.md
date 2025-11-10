---
title: "Réunion des développeurs d’I2P - 11 novembre 2003"
date: 2003-11-11
author: "jrand0m"
description: "Réunion de développement I2P portant sur le statut du router, les mises à jour de la feuille de route, l’implémentation native de modPow, le programme d’installation graphique, et des discussions sur les licences"
categories: ["meeting"]
---

(Avec l'aimable autorisation de la wayback machine http://www.archive.org/)

## Récapitulatif rapide

<p class="attendees-inline"><strong>Présents:</strong> dish, dm, jrand0m, MrEcho, nop</p>

(journal de réunion modifié pour masquer le fait que iip a planté en plein milieu de la réunion et qu'il y a eu beaucoup d'expirations de délai de ping, donc n'essayez pas de lire ceci comme un récit linéaire)

## Journal de réunion

<div class="irc-log"> [22:02] &lt;jrand0m&gt; ordre du jour [22:02] &lt;jrand0m&gt; 0) bienvenue [22:02] &lt;jrand0m&gt; 1) i2p router [22:02] &lt;jrand0m&gt; 1.1) état [22:02] &lt;jrand0m&gt; 1.2) modifications de la feuille de route [22:02] &lt;jrand0m&gt; 1.3) sous-projets ouverts [22:02] &lt;jrand0m&gt; 2) modPow natif [22:03] &lt;jrand0m&gt; 2) programme d'installation GUI [22:03] &lt;jrand0m&gt; 3) messagerie instantanée (IM) [22:03] &lt;jrand0m&gt; 4) service de noms [22:03] &lt;MrEcho&gt; j'ai vu ce code .c [22:03] &lt;jrand0m&gt; 5) licences [22:03] &lt;jrand0m&gt; 6) autre ? [22:03] &lt;jrand0m&gt; 0) bienvenue [22:03] &lt;jrand0m&gt; salut. [22:03] &lt;nop&gt; salut [22:03] &lt;jrand0m&gt; réunion 2^6 [22:04] &lt;jrand0m&gt; tu as des points à ajouter à l'ordre du jour, nop ? [22:04] &lt;jrand0m&gt; ok, 1.1) état du router [22:04] &lt;jrand0m&gt; on est en 0.2.0.3 et d'après les dernières nouvelles, c'est fonctionnel [22:04] &lt;MrEcho&gt; &gt; 0.2.0.3 [22:04] &lt;MrEcho&gt; c'est bien ça ? [22:05] &lt;MrEcho&gt; je le fais tourner... ça a l'air bien [22:05] &lt;nop&gt; non [22:05] &lt;jrand0m&gt; il y a eu de petits commits après la version 0.2.0.3, rien qui vaille une nouvelle version [22:05] &lt;nop&gt; j'essaie juste de rattraper [22:05] &lt;jrand0m&gt; cool [22:06] &lt;jrand0m&gt; vu les expériences et retours de la 0.2.0.x, la feuille de route a été mise à jour pour rendre l'exécution moins gourmande en ressources [22:06] &lt;jrand0m&gt; (c.-à-d. pour que les gens puissent faire tourner des serveurs web / etc. sans que ça leur bouffe le CPU) [22:06] &lt;jrand0m&gt; plus précisément (on passe au point 1.2 de l'ordre du jour) : http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap [22:06] &lt;MrEcho&gt; ce que j'ai remarqué, c'est que la plupart des routers utilisent : TransportStyle: PHTTP [22:07] &lt;MrEcho&gt; ça passe automatiquement en PHTTP ou ça essaie d'abord TCP ? [22:07] &lt;jrand0m&gt; hmm, la plupart des routers devraient supporter PHTTP, et s'ils peuvent accepter des connexions entrantes, ils devraient supporter TCP aussi [22:07] &lt;jrand0m&gt; si c'est possible, il utilise TCP [22:07] &lt;jrand0m&gt; PHTTP est pondéré comme environ 1000 fois plus coûteux que TCP [22:08] &lt;jrand0m&gt; (voir GetBidsJob, qui demande à chaque transport combien il pense que ça coûterait d'envoyer un message à un pair) [22:08] &lt;jrand0m&gt; (et voir TCPTransport.getBid et PHTTPTransport.getBid pour les valeurs utilisées) [22:08] &lt;MrEcho&gt; ok [22:08] &lt;jrand0m&gt; utilises-tu souvent PHTTP pour envoyer et recevoir des messages ? [22:09] &lt;jrand0m&gt; (ça peut être le signe que ton écouteur TCP n'est pas joignable) [22:09] &lt;MrEcho&gt; je n'ai pas mis les URLs de mon côté [22:09] &lt;jrand0m&gt; ah ok. [22:09] &lt;MrEcho&gt; oh si, il l'est [22:10] &lt;jrand0m&gt; ok, ouais, mes routers ont des connexions TCP ouvertes vers toi [22:10] &lt;dm&gt; comme c'est hospitalier de leur part. [22:10] * jrand0m est content que vous m'ayez fait implémenter routerConsole.html pour qu'on n'ait pas à fouiller dans les logs pour cette merde [22:11] &lt;MrEcho&gt; y a-t-il un timeout qui fait que s'il ne se connecte pas en TCP il passe en PHTTP ? et c'est quoi le timing ? [22:11] &lt;jrand0m&gt; mais bref, le grand changement de la feuille de route, c'est que la 0.2.1 implémentera le truc AES+SessionTag [22:11] &lt;MrEcho&gt; ou on pourrait avoir ça dans un réglage ? [22:11] &lt;jrand0m&gt; s'il reçoit un refus de connexion TCP / hôte introuvable / etc., il abandonne immédiatement cette tentative et essaie la prochaine offre disponible [22:12] &lt;MrEcho&gt; donc pas de nouvelles tentatives [22:12] &lt;jrand0m&gt; PHTTP a un timeout de 30 s, si je me souviens bien [22:12] &lt;jrand0m&gt; pas besoin de réessayer. soit tu as une connexion TCP ouverte et tu peux envoyer les données, soit non :) [22:12] &lt;MrEcho&gt; lol ok [22:13] &lt;MrEcho&gt; est-ce qu'il retentera TCP à chaque fois après ça, ou bien il sautera et passera directement en PHTTP pour la connexion suivante ? [22:13] &lt;jrand0m&gt; pour le moment, il tente TCP à chaque fois. [22:13] &lt;jrand0m&gt; les transports ne conservent pas encore d'historique [22:13] &lt;MrEcho&gt; ok cool [22:14] &lt;jrand0m&gt; (mais si un pair échoue 4 fois, il est mis sur la shitlist pendant 8 minutes) [22:14] &lt;MrEcho&gt; eh bien une fois que l'autre côté reçoit le message PHTTP, il devrait se connecter au router qui a envoyé le message via TCP, non ? [22:14] &lt;jrand0m&gt; correct. une fois qu'une connexion TCP est établie, il peut l'utiliser. [22:14] &lt;jrand0m&gt; (mais si les deux pairs n'ont que PHTTP, ils utiliseront évidemment uniquement PHTTP) [22:15] &lt;MrEcho&gt; ça voudrait dire qu'il ne pouvait établir de connexion TCP vers quoi que ce soit [22:15] &lt;MrEcho&gt; .. mais ouais [22:16] &lt;MrEcho&gt; j'aimerais qu'il y ait un moyen de contourner ça [22:16] &lt;jrand0m&gt; non, un de mes routers n'a pas d'adresse TCP - seulement PHTTP. mais j'établis des connexions TCP avec des pairs qui ont des adresses TCP. [22:16] &lt;jrand0m&gt; (et ensuite ils peuvent renvoyer des messages via cette connexion TCP plutôt que de m'envoyer des messages PHTTP plus lents) [22:17] &lt;jrand0m&gt; ou ce n'est pas ce que tu voulais dire ? [22:17] &lt;MrEcho&gt; ouais je me suis embrouillé [22:17] &lt;jrand0m&gt; yep, pas de souci [22:18] &lt;jrand0m&gt; donc, voir la feuille de route mise à jour pour les infos de planning mises à jour ((Link: http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap)http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap) [22:18] &lt;jrand0m&gt; ok, 1.3) sous-projets ouverts [22:19] &lt;jrand0m&gt; j'ai enfin mis une partie de la liste de choses à faire de mon palmpilot dans le wiki à (Link: http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects)http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects [22:19] &lt;jrand0m&gt; donc si tu t'ennuies et que tu cherches des projets de code... :) [22:19] &lt;MrEcho&gt; pff [22:20] &lt;MrEcho&gt; j'en ai déjà 2 [22:20] &lt;dish&gt; Tu as un palmpilot, c'est la classe [22:20] &lt;MrEcho&gt; le mien est mort [22:20] &lt;jrand0m&gt; mihi&gt; il y a un point là-dedans concernant l'I2PTunnel décrivant une idée que j'ai eue il y a quelque temps [22:20] &lt;MrEcho&gt; je sais pas ce qu'il a [22:21] &lt;jrand0m&gt; ouais, j'avais des palms avant mais on m'a récemment donné celui-ci pour la cause ;) [22:21] &lt;dish&gt; Pourrait-on avoir un point à l'ordre du jour de la réunion pour discuter de la dernière fois où userX a tapé quelque chose [22:21] &lt;MrEcho&gt; ce foutu truc ne s'allume même plus [22:21] &lt;MrEcho&gt; lol [22:22] &lt;jrand0m&gt; je ne pense pas que UserX ait dit quoi que ce soit depuis 4 ou 5 mois ;) [22:22] &lt;MrEcho&gt; c'est un bot ou quoi ? [22:22] &lt;dish&gt; Qu'est-ce qu'il a dit il y a 5 mois ? [22:22] &lt;MrEcho&gt; je parie que c'est un bitchx qui tourne sur une machine à laquelle il avait accès... et qu'il a oubliée [22:22] &lt;jrand0m&gt; qu'il reviendrait avec des commentaires sur l'anonCommFramework (ancien nom d'i2p) la semaine suivante ;) [22:23] &lt;dish&gt; haha [22:23] &lt;jrand0m&gt; mais je suppose qu'il est occupé. c'est la vie [22:23] &lt;jrand0m&gt; ok, 2) modPow natif [22:23] &lt;MrEcho&gt; j'ai vu ce code c [22:24] &lt;jrand0m&gt; j'ai assemblé un .c stub et une classe Java pour montrer comment quelque chose comme GMP ou une autre bibliothèque MPI pourrait être intégré, mais évidemment ça ne marche pas [22:25] &lt;jrand0m&gt; ce qui serait bien, ce serait d'avoir un petit paquet de classes C et cette classe d'enveloppe Java triviale associée que l'on pourrait compiler pour Windows, OSX, *BSD, Linux, et empaqueter sous GPL

(insérer ici une défaillance majeure d'iip)

[22:38] &lt;MrEcho&gt; la dernière chose que j’ai vue était : [13:25] &lt;jrand0m&gt; ok, 2) native modPow
[22:38] &lt;jrand0m&gt; salut MrEcho
[22:38] &lt;jrand0m&gt; ouais, on dirait qu’un proxy principal a planté
[22:39] &lt;jrand0m&gt; je lui laisse encore 2 min avant de redémarrer
[22:39] &lt;MrEcho&gt; ok
[22:39] &lt;MrEcho&gt; pour 25 $ une fois je peux avoir Java complet sur thenidus.net ... un de mes sites
[22:40] &lt;jrand0m&gt; 25 $ ? ils te facturent l’installation de logiciels ?
[22:40] &lt;MrEcho&gt; aucune idée en fait... c’est un forfait
[22:40] &lt;MrEcho&gt; je parle à mon pote là tout de suite
[22:40] &lt;jrand0m&gt; je ne suis pas sûr que le code soit assez stable pour aller louer une flopée d’emplacements en colocation pour y déployer des routers. pas encore :)
[22:41] &lt;dm&gt; un forfait de quoi ?
[22:41] &lt;MrEcho&gt; java - jsp
[22:41] &lt;jrand0m&gt; ok, je renvoie ce que j’ai envoyé avant :
[22:41] &lt;jrand0m&gt; j’ai bricolé un stub en .c et une classe Java pour montrer comment quelque chose comme GMP ou une autre bibliothèque MPI pourrait être intégré, mais ça ne marche évidemment pas
[22:41] &lt;jrand0m&gt; ce qui serait bien, ce serait d’avoir un petit paquet de classes C et la classe wrapper Java triviale associée, que l’on pourrait compiler pour windows, osx, *bsd, linux, et empaqueter sous GPL (ou une licence moins restrictive)
[22:41] &lt;jrand0m&gt; toutefois, avec la nouvelle feuille de route qui met AES+SessionTag comme tâche en cours pour moi, ce n’est plus aussi critique qu’avant.
[22:42] &lt;jrand0m&gt; si quelqu’un veut s’en charger malgré tout, ce serait super (et je suis sûr qu’un autre projet que nous connaissons tous serait intéressé par un tel packaging)
[22:43] &lt;dm&gt; frazaa ?
[22:43] &lt;jrand0m&gt; hé, d’une certaine façon ;)
[22:44] &lt;jrand0m&gt; ok, 3) installateur GUI
[22:44] &lt;jrand0m&gt; MrEcho&gt; salut
[22:44] &lt;MrEcho&gt; :)
[22:44] &lt;MrEcho&gt; héhé
[22:44] &lt;MrEcho&gt; ça avance
[22:44] &lt;jrand0m&gt; cool
[22:44] &lt;MrEcho&gt; rien de spécial
[22:45] &lt;MrEcho&gt; j’ai des idées vraiment cool pour le rendre super chiadé... mais c’est pour plus tard
[22:45] &lt;jrand0m&gt; je me demandais si l’installateur devait ajouter 1) une option pour récupérer automatiquement les seeds depuis http://.../i2pdb/ 2) récupérer automatiquement http://.../i2p/squid.dest et créer aussi un runSquid.bat/runSquid.sh ?
[22:45] &lt;jrand0m&gt; ouais
[22:46] &lt;jrand0m&gt; ouais, on veut que l’installateur soit le plus simple possible — tu pensais à quoi comme trucs « fancy » ?
[22:46] &lt;MrEcho&gt; la question, c’est que quand tu fais java -jar installer ça part sur le non-GUI par défaut à cause de la façon dont tu as organisé les choses
[22:46] &lt;MrEcho&gt; comment on fait pour que quand tu double-cliques le fichier jar ça lance la GUI
[22:47] &lt;jrand0m&gt; install.jar &lt;-- non-GUI,  installgui.jar &lt;-- GUI
[22:47] &lt;jrand0m&gt; code séparé, paquets séparés
[22:47] &lt;MrEcho&gt; « fancy » au sens de trucs que tu ne remarqueras peut-être pas... mais ça va être propre et soigné
[22:47] &lt;jrand0m&gt; cool
[22:47] &lt;MrEcho&gt; ah ok
[22:48] &lt;jrand0m&gt; (ou install &lt;-- GUI, installcli &lt;-- CLI. on verra comment ça évolue)
[22:49] &lt;jrand0m&gt; autre chose sur la GUI, ou on passe au point 4) ?
[22:49] &lt;jrand0m&gt; (tu as une idée du délai ? pas de pression, je demande juste)
[22:51] &lt;MrEcho&gt; aucune idée pour l’instant
[22:51] &lt;jrand0m&gt; cool
[22:51] &lt;jrand0m&gt; ok, 4) IM (messagerie instantanée)
[22:51] &lt;jrand0m&gt; thecrypto n’est pas là, donc.....
[22:51] &lt;jrand0m&gt; 5) service de nommage
[22:51] &lt;jrand0m&gt; wiht n’est pas là non plus...
[22:51] &lt;jrand0m&gt; ping
[22:52] &lt;dish&gt; tu t’es trompé dans la numérotation de l’ordre du jour
[22:52] &lt;dish&gt; 3) IM
[22:52] &lt;jrand0m&gt; ouais, j’avais l’habitude d’avoir deux points 2 à l’ordre du jour
[22:52] &lt;dish&gt; 4) Nommage
[22:52] &lt;dish&gt; ;)
[22:52] &lt;jrand0m&gt; (native modPow et installateur GUI)
[22:52] &lt;jrand0m&gt; tu vois, on est dynamiques et tout
[22:59] &lt;jrand0m&gt; ok, pour les logs je suppose que je vais continuer
[22:59] &lt;jrand0m&gt; 6) licences
[23:00] &lt;jrand0m&gt; je pense aller vers quelque chose de moins restrictif que la GPL. on utilise du code MIT, plus un autre fichier qui est GPL (mais c’est juste l’encodage base64 et ça peut être remplacé facilement). à part ça, tout le code est sous copyright soit par moi, soit par thecrypto.
[23:00] * dish regarde la partie du code i2p tunnel de mihi
[23:01] &lt;jrand0m&gt; ah oui, mihi a publié ça sous GPL mais il peut vouloir le publier sous autre chose s’il le souhaite aussi
[23:01] &lt;jrand0m&gt; (mais i2ptunnel est essentiellement une appli tierce et peut choisir la licence qu’elle veut)
[23:02] &lt;jrand0m&gt; (bien que, puisque le SDK i2p est GPL, il a été forcé d’être en GPL)
[23:02] &lt;MrEcho&gt; zut, il était temps
[23:02] &lt;jrand0m&gt; je ne sais pas. les licences, ce n’est pas mon fort, mais je serais enclin au moins à passer en LGPL
[23:02] * dish publie les 10–20 lignes de modification du code I2P HTTP Client de mihi sous la licence qu’utilise mihi, quelle qu’elle soit
[23:03] &lt;jrand0m&gt; héhé :)
[23:06] &lt;jrand0m&gt; bref, 7) autre ?
[23:07] &lt;jrand0m&gt; quelqu’un a des questions / préoccupations / idées à propos d’i2p ?
[23:07] &lt;dish&gt; Laissez-moi poser une question
[23:07] &lt;dish&gt; Est-ce que I2P a une fonctionnalité de nom de groupe ?
[23:07] &lt;jrand0m&gt; une fonctionnalité de nom de groupe ?
[23:07] &lt;dm&gt; équipe Discovery Channel !
[23:07] &lt;MrEcho&gt; lol
[23:08] &lt;dish&gt; L’idée étant que si tu veux avoir un réseau privé ou séparé, mais que certains router se mélangent d’une manière ou d’une autre, sans nom de groupe les deux réseaux fusionneraient
[23:08] &lt;MrEcho&gt; il pense à Waste
[23:08] &lt;jrand0m&gt; ah
[23:08] &lt;dish&gt; Je ne sais pas pourquoi on voudrait ça, mais je demande au cas où
[23:08] &lt;jrand0m&gt; oui, au début de la conception du réseau je jouais avec cette idée
[23:09] &lt;jrand0m&gt; c’est plus avancé que ce dont on a besoin pour l’instant (ou dans un futur relativement proche [6–12 mois]) mais ça pourrait être intégré plus tard
[23:09] &lt;dish&gt; Ou bien est-ce une mauvaise idée parce qu’il vaut mieux garder un seul grand réseau
[23:09] &lt;dm&gt; i2pisdead
[23:09] &lt;jrand0m&gt; hé dm
[23:10] &lt;nop&gt; ferme-la
[23:10] &lt;jrand0m&gt; non dish, c’est une bonne idée
[23:10] &lt;dm&gt; nop : gros dur ?
[23:10] &lt;jrand0m&gt; c’est essentiellement ce qu’est la version 0.2.3 — routes restreintes
[23:10] &lt;jrand0m&gt; (a.k.a. tu as un petit ensemble privé (de confiance) de pairs et tu ne veux pas que tout le monde sache qui ils sont, mais tu veux quand même pouvoir communiquer avec eux)
[23:15] &lt;jrand0m&gt; ok, autre chose ?
[23:15] &lt;nop&gt; non, je fais juste le clown
[23:18] &lt;dm&gt; marrant, hein ?
[23:20] &lt;jrand0m&gt; ok, eh bien, réunion /intéressante/, avec quelques plantages iip au milieu ;)
[23:21] * jrand0m *baf* met fin à la réunion </div>
