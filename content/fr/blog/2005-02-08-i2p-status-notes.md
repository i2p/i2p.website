---
title: "Notes sur l'état d'I2P du 2005-02-08"
date: 2005-02-08
author: "jr"
description: "Notes hebdomadaires sur l’état du développement d’I2P couvrant les mises à jour 0.4.2.6, les progrès du tunnel 0.5 avec des filtres de Bloom, i2p-bt 0.1.6 et le Fortuna PRNG"
categories: ["status"]
---

Salut tout le monde, c'est encore l'heure de la mise à jour

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

On ne dirait pas, mais cela fait plus d’un mois que la version 0.4.2.6 est sortie et la situation est toujours plutôt bonne. Il y a eu depuis toute une série de mises à jour bien utiles [1], mais rien de vraiment bloquant nécessitant de pousser une nouvelle version. Cependant, au cours du dernier jour ou deux, nous avons reçu de très bonnes corrections de bugs (merci anon et Sugadude !), et si nous n’étions pas sur le point de publier la 0.5, je l’emballerais probablement et la sortirais. La mise à jour d’anon corrige un cas limite dans la bibliothèque de streaming qui provoquait bon nombre des expirations observées dans BT (BitTorrent) et d’autres transferts volumineux, donc si vous vous sentez d’humeur aventureuse, récupérez CVS HEAD et essayez-la. Ou attendez simplement la prochaine version, bien sûr.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

Énormément de progrès du côté de la 0.5 (comme quiconque sur la liste i2p-cvs [2] pourra en attester). Toutes les mises à jour des tunnels et divers réglages de performances ont été testés, et bien que cela n'inclue pas grand-chose en matière de divers [3] algorithmes d'ordonnancement imposés, cela couvre l’essentiel. Nous avons également intégré un ensemble de (sous licence BSD) filtres de Bloom [4] provenant de XLattice [5], ce qui nous permet de détecter les attaques par rejeu sans nécessiter aucune utilisation de mémoire par message et avec une surcharge proche de 0ms. Pour répondre à nos besoins, les filtres ont été simplement étendus pour intégrer une décroissance, de sorte qu’après l’expiration d’un tunnel, le filtre n’ait plus les IV (vecteurs d’initialisation) que nous avons vus dans ce tunnel.

Alors que j’essaie d’intégrer autant de choses que possible dans la version 0.5, je me rends aussi compte que nous devons prévoir l’imprévisible - autrement dit, la meilleure façon de l’améliorer est de vous la mettre entre les mains et d’apprendre de la manière dont elle fonctionne (et ne fonctionne pas) pour vous.  Pour aider à cela, comme je l’ai déjà mentionné, nous allons publier une version 0.5 (avec un peu de chance d’ici la semaine prochaine), qui rompt la rétrocompatibilité, puis nous travaillerons à l’améliorer à partir de là, en préparant une version 0.5.1 lorsqu’elle sera prête.

En revenant sur la feuille de route [6], la seule chose reportée à la 0.5.1 est l'ordre strict.  Il y aura également des améliorations concernant la limitation du débit et l'équilibrage de charge au fil du temps, j'en suis sûr, mais je m'attends à ce que nous l'affinions pratiquement indéfiniment.  On a cependant discuté d'autres éléments que j'espérais inclure dans la 0.5, comme l'outil de téléchargement et le code de mise à jour en un clic, mais il semble qu'ils seront eux aussi reportés.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck a publié une nouvelle version corrigée d'i2p-bt (youpi !), disponible aux emplacements habituels ; procurez-vous-la tant que c'est tout chaud [7].  Entre cette mise à jour et le correctif de la bibliothèque de streaming d'anon, j'ai pratiquement saturé ma liaison montante en seedant quelques fichiers, alors tentez le coup.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

Comme mentionné lors de la réunion de la semaine dernière, smeghead abat en ce moment un travail considérable sur toute une série de mises à jour et, en luttant pour faire fonctionner I2P avec gcj, des problèmes de PRNG (générateur pseudo-aléatoire) vraiment épouvantables sont apparus dans certaines JVM (machines virtuelles Java), nous contraignant pratiquement à adopter un PRNG sur lequel nous pouvons compter. Après avoir reçu un retour de l’équipe GNU-Crypto, même si leur implémentation de Fortuna n’a pas encore vraiment été déployée, elle semble être la mieux adaptée à nos besoins. Nous pourrions réussir à l’intégrer à la version 0.5, mais il y a de fortes chances que ce soit reporté à la 0.5.1, car nous voudrons l’ajuster afin qu’elle puisse nous fournir la quantité nécessaire de données aléatoires.

* 5) ???

Beaucoup de choses se passent, et il y a eu récemment un regain d’activité sur le forum [8] aussi, donc je suis sûr d’avoir manqué certaines choses. Quoi qu’il en soit, passez faire un tour à la réunion dans quelques minutes et dites ce que vous avez en tête (ou restez en sous-marin et lâchez une remarque sarcastique au hasard).

=jr [8] http://forum.i2p.net/
