---
title: "Notes de statut I2P du 2005-08-16"
date: 2005-08-16
author: "jr"
description: "Brève mise à jour couvrant l'état de PeerTest, la transition du réseau Irc2P, l'avancement de l'interface graphique de Feedspace et le changement de l'heure de la réunion à 20 h GMT"
categories: ["status"]
---

Salut tout le monde, quelques notes rapides aujourd'hui

* Index:

1) statut de PeerTest 2) Irc2P 3) Feedspace 4) méta 5) ???

* 1) PeerTest status

Comme mentionné précédemment, la version 0.6.1 à venir inclura une série de tests pour configurer plus finement le router et vérifier la joignabilité (ou indiquer ce qu’il faut faire), et bien que nous ayons du code dans CVS depuis deux builds maintenant, il reste encore quelques affinements avant que cela fonctionne aussi bien que nécessaire. En ce moment, j’apporte quelques modifications mineures au flux de test documenté [1] en ajoutant un paquet supplémentaire pour vérifier la joignabilité de Charlie et en retardant la réponse de Bob à Alice jusqu’à ce que Charlie ait répondu. Cela devrait réduire le nombre de valeurs de statut "ERR-Reject" inutiles que les gens voient, puisque Bob ne répondra pas à Alice tant qu’il n’aura pas un Charlie prêt pour le test (et lorsque Bob ne répond pas, Alice voit "Unknown" comme statut).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

Bon, voilà, c'est tout - la 0.6.0.2-3 devrait sortir demain, et elle sera publiée en tant que version une fois qu'elle aura été testée de manière approfondie.

* 2) Irc2P

Comme mentionné sur le forum [2], les utilisateurs d'I2P qui utilisent l'IRC doivent mettre à jour leur configuration pour passer au nouveau réseau IRC. Duck sera temporairement hors ligne pour [redacted], et plutôt que d'espérer que le serveur ne rencontre pas de problème pendant ce temps, postman et smeghead ont pris le relais et mis en place un nouveau réseau IRC à votre disposition. Postman a également mis en miroir le tracker de duck et le site i2p-bt à l'adresse [3], et il me semble avoir vu quelque chose sur le nouveau réseau IRC au sujet de susi qui lance une nouvelle instance d'IdleRPG (consultez la liste des canaux pour plus d'informations).

Mes remerciements vont à ceux qui étaient responsables de l’ancien réseau i2pirc (duck, baffled, l’équipe metropipe, postman) et à ceux qui sont responsables du nouveau réseau irc2p (postman, arcturus) ! Des services et des contenus intéressants donnent tout son intérêt à I2P, et c’est à vous de les créer !

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

À ce propos, je parcourais le blog de frosk l’autre jour et il semble qu’il y ait encore des progrès sur Feedspace — notamment une chouette petite interface graphique. Je sais que ce n’est peut‑être pas encore prêt à être testé, mais je suis sûr que frosk nous passera du code le moment venu. Au passage, j’ai aussi entendu une rumeur au sujet d’un autre outil de blog Web respectueux de l’anonymat, actuellement dans les tuyaux, qui pourra s’intégrer à Feedspace quand ce sera prêt, mais là encore, je suis sûr qu’on en saura plus quand ce sera prêt.

* 4) meta

Étant le sale égoïste que je suis, j’aimerais avancer un peu les réunions - au lieu de 21h GMT, essayons 20h GMT. Pourquoi ? Parce que ça convient mieux à mon emploi du temps ;) (les cybercafés les plus proches ne restent pas ouverts trop tard).

* 5) ???

C'est à peu près tout pour le moment - je vais essayer d'être près d'un cybercafé pour la réunion de ce soir, donc n'hésitez pas à passer sur #i2p à *8*P GMT sur les serveurs irc /new/ {irc.postman.i2p, irc.arcturus.i2p}. Nous pourrions avoir un bot changate en ligne vers irc.freenode.net - quelqu'un veut en faire tourner un ?

salut, =jr
