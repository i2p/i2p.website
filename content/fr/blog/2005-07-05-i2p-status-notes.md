---
title: "Notes de statut I2P du 2005-07-05"
date: 2005-07-05
author: "jr"
description: "Mise à jour hebdomadaire couvrant l'avancement du transport SSU, l'atténuation des attaques sur l'IV (vecteur d'initialisation) du tunnel, et l'optimisation du MAC SSU avec HMAC-MD5"
categories: ["status"]
---

Salut la bande, c'est encore ce moment de la semaine,

* Index

1) Dev status 2) Tunnel IVs 3) SSU MACs 4) ???

* 1) Dev status

Encore une semaine, encore un message disant "Il y a eu beaucoup de progrès sur le transport SSU" ;) Mes modifications locales sont stables et ont été envoyées dans CVS (HEAD est à 0.5.0.7-9), mais aucune version n'a encore été publiée. Plus de nouvelles sur ce front bientôt. Les détails concernant les changements non liés à SSU sont dans l'historique [1], même si je garde pour l'instant les changements liés à SSU en dehors de cette liste, puisque SSU n'est encore utilisé par aucun non-développeur (et les développeurs lisent i2p-cvs@ :)

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) Tunnel IVs

Depuis quelques jours, dvorak publie des réflexions occasionnelles sur différentes manières d’attaquer le chiffrement du tunnel et, même si la plupart avaient déjà été traitées, nous avons pu élaborer un scénario qui permettrait aux participants de marquer une paire de messages afin de déterminer qu’ils empruntent le même tunnel. Le fonctionnement était le suivant : le premier pair laissait passer un message, puis, plus tard, il réutilisait le vecteur d’initialisation (IV) et le premier bloc de données de ce premier message du tunnel pour les insérer dans un nouveau. Ce nouveau message serait bien sûr corrompu, mais il ne serait pas identifié comme une attaque par rejeu (replay), puisque les IV seraient différents. Plus loin, le second pair pouvait alors simplement rejeter ce message, de sorte que l’extrémité du tunnel ne puisse pas détecter l’attaque.

L’un des problèmes fondamentaux sous-jacents est qu’il n’existe aucun moyen de vérifier un message de tunnel au fur et à mesure qu’il parcourt le tunnel sans ouvrir la porte à toute une série d’attaques (voir une proposition antérieure de chiffrement de tunnel [2] pour une méthode qui s’en approche, mais dont les probabilités sont assez douteuses et qui impose certaines limites artificielles aux tunnels).

[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

Il existe cependant un moyen trivial de contourner l’attaque particulière décrite - il suffit de considérer xor(IV, premier bloc de données) comme l’identifiant unique passé par le filtre de Bloom au lieu de l’IV (vecteur d’initiation) seul. De cette façon, les pairs intermédiaires verront le doublon et le rejetteront avant qu’il n’atteigne le deuxième pair de connivence. CVS a été mis à jour pour inclure cette contre-mesure, bien que je doute très, très fortement qu’il s’agisse d’une menace pratique compte tenu de la taille actuelle du réseau, donc je ne la publie pas comme une version autonome.

Cela n’affecte toutefois pas la viabilité d’autres attaques de temporisation ou de shaping (mise en forme du trafic), mais il vaut mieux éliminer les attaques faciles à gérer dès qu’on les repère.

* 3) SSU MACs

Comme décrit dans la spécification [3], le transport SSU utilise un MAC (code d’authentification de message) pour chaque datagramme transmis. Cela s’ajoute au hachage de vérification envoyé avec chaque message I2NP (ainsi qu’aux hachages de vérification de bout en bout sur les messages clients). À l’heure actuelle, la spécification et le code utilisent un HMAC-SHA256 tronqué – en ne transmettant et ne vérifiant que les 16 premiers octets du MAC. C’est *tousse* un peu du gaspillage, car le HMAC utilise la fonction de hachage SHA256 deux fois dans son opération, en travaillant à chaque fois avec un hachage de 32 octets, et un profilage récent du transport SSU suggère que cela se situe près du chemin critique pour la charge CPU. En conséquence, j’ai un peu exploré le remplacement de HMAC-SHA256-128 par un HMAC-MD5(-128) simple – bien que MD5 ne soit clairement pas aussi solide que SHA256, nous tronquons de toute façon le SHA256 à la même taille que MD5, donc la quantité de force brute nécessaire pour une collision est la même (2^64 tentatives). Je fais des essais en ce moment et l’accélération est substantielle (obtenant plus de 3x le débit HMAC sur des paquets de 2KB par rapport à SHA256), donc nous pourrions peut-être le déployer en production à la place. Ou si quelqu’un peut avancer une excellente raison de ne pas le faire (ou une meilleure alternative), il est assez simple d’en changer (une seule ligne de code).

[3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 4) ???

C’est à peu près tout pour le moment et, comme toujours, n’hésitez pas à poster vos idées et préoccupations quand vous voulez. CVS HEAD est de nouveau compilable pour ceux qui n’ont pas junit installé (pour le moment j’ai retiré les tests du fichier i2p.jar, mais ils restent exécutables avec la cible ant test), et je m’attends à ce qu’il y ait bientôt plus de nouvelles au sujet des tests de la 0.6 (je me bats encore avec les bizarreries de la colo box (serveur en colocation) en ce moment - me connecter en telnet à mes propres interfaces échoue en local (sans errno utile), ça fonctionne à distance, le tout sans iptables ni autres filtres. joie). Je n’ai toujours pas d’accès Internet @ home, donc je ne serai pas là pour une réunion ce soir, mais peut-être la semaine prochaine.

=jr
