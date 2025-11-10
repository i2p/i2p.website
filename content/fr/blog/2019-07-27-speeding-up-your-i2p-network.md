---
title: "Accélérer votre réseau I2P"
date: 2019-07-27
author: "mhatta"
description: "Accélérer votre réseau I2P"
categories: ["tutorial"]
---

*Cet article est adapté directement à partir de contenu initialement créé pour le* [blog Medium](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *.* *Le mérite pour l'article original lui revient. Il a été mis à jour à certains endroits où* *il fait référence à d'anciennes versions d'I2P comme actuelles et a fait l'objet d'un léger* *travail d'édition. -idk*

Juste après son démarrage, I2P est souvent perçu comme un peu lent. C'est vrai, et nous savons tous pourquoi : par nature, [garlic routing (routage « garlic »)](https://en.wikipedia.org/wiki/Garlic_routing) ajoute un surcoût à l'expérience familière de l'utilisation d'Internet afin que vous puissiez préserver votre vie privée, mais cela signifie que, pour de nombreux services I2P, voire la plupart, vos données devront, par défaut, passer par 12 sauts.

![Analyse des outils d’anonymat en ligne](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

De plus, contrairement à Tor, I2P a été conçu principalement comme un réseau fermé. Vous pouvez facilement accéder aux [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) ou à d’autres ressources à l’intérieur d’I2P, mais il n’est pas prévu d’accéder à des sites [clearnet](https://en.wikipedia.org/wiki/Clearnet_(networking)) (Internet clair) via I2P. Il existe quelques I2P "outproxies" (mandataires sortants) similaires aux nœuds de sortie de [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network)) pour accéder au clearnet, mais la plupart sont très lents à utiliser, car aller vers le clearnet constitue en pratique *un autre* saut dans une connexion qui comporte déjà 6 sauts à l’entrée et six sauts à la sortie.

Jusqu’à il y a quelques versions, ce problème était encore plus difficile à gérer, car de nombreux utilisateurs du router I2P avaient des difficultés à configurer les paramètres de bande passante de leur router. Si tous ceux qui le peuvent prennent le temps d’ajuster correctement leurs paramètres de bande passante, ils amélioreront non seulement votre connexion, mais aussi le réseau I2P dans son ensemble.

## Ajustement des limites de bande passante

Puisque I2P est un réseau pair à pair, vous devez partager une partie de votre bande passante réseau avec d'autres pairs. Vous pouvez configurer ce montant dans « I2P Bandwidth Configuration » (bouton « Configure Bandwidth » dans la section « Applications and Configuration » de l'I2P Router Console, ou http://localhost:7657/config).

![Configuration de la bande passante d'I2P](https://geti2p.net/images/blog/bandwidthmenu.png)

Si vous voyez une limite de bande passante partagée de 48 KBps, ce qui est très faible, il se peut que vous n’ayez pas ajusté votre bande passante partagée par rapport à la valeur par défaut. Comme l’auteur original du matériel dont est adapté cet article de blog l’a souligné, I2P définit par défaut une limite de bande passante partagée très faible, jusqu’à ce que l’utilisateur l’ajuste, afin d’éviter de perturber la connexion de l’utilisateur.

Cependant, comme de nombreux utilisateurs peuvent ne pas savoir exactement quels paramètres de bande passante ajuster, la [version 0.9.38 d’I2P](https://geti2p.net/en/download) a introduit un Assistant de première installation. Il contient un Test de bande passante, qui détecte automatiquement (grâce au [NDT](https://www.measurementlab.net/tests/ndt/) de M-Lab) et ajuste en conséquence les paramètres de bande passante d’I2P.

Si vous souhaitez relancer l’assistant de configuration, par exemple après un changement de fournisseur d’accès ou parce que vous avez installé I2P avant la version 0.9.38, vous pouvez le relancer depuis le lien 'Setup' sur la page 'Help & FAQ', ou simplement accéder directement à l’assistant à l’adresse http://localhost:7657/welcome

![Pouvez-vous trouver « Setup » ?](https://geti2p.net/images/blog/sidemenu.png)

L'utilisation de l'assistant est simple, il suffit de continuer à cliquer sur "Next". Parfois, les serveurs de mesure choisis par M-Lab sont hors service et le test échoue. Dans ce cas, cliquez sur "Previous" (n'utilisez pas le bouton "back" de votre navigateur web), puis réessayez.

![Résultats du test de bande passante](https://geti2p.net/images/blog/bwresults.png)

## Exécution continue d'I2P

Même après avoir ajusté la bande passante, votre connexion peut rester lente. Comme je l’ai dit, I2P est un réseau P2P. Il faudra un certain temps pour que votre I2P router soit découvert par d’autres pairs et intégré au réseau I2P. Si votre router n’est pas resté en ligne suffisamment longtemps pour être bien intégré, ou si vous l’arrêtez brutalement trop souvent, le réseau restera plutôt lent. À l’inverse, plus vous laissez votre I2P router fonctionner en continu, plus votre connexion devient rapide et stable, et une plus grande part de votre bande passante sera utilisée sur le réseau.

Toutefois, beaucoup de personnes pourraient ne pas pouvoir maintenir votre I2P router en ligne. Dans ce cas, vous pouvez quand même exécuter l’I2P router sur un serveur distant tel qu’un VPS, puis utiliser le transfert de port SSH.
