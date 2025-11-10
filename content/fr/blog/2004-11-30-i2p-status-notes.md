---
title: "Notes d'état d'I2P du 2004-11-30"
date: 2004-11-30
author: "jr"
description: "Mise à jour hebdomadaire de l'état d'I2P couvrant les versions 0.4.2 et 0.4.2.1, les développements de mail.i2p, les avancées d'i2p-bt et les discussions sur la sécurité des eepsite"
categories: ["status"]
---

Salut à tous

## Index

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 et 0.4.2.1

Depuis que nous avons enfin publié la version 0.4.2, la fiabilité et le débit du réseau ont fortement augmenté pendant un moment, jusqu’à ce que nous tombions sur les tout nouveaux bogues que nous avions créés. Pour la plupart des utilisateurs, les connexions IRC durent des heures d’affilée, mais pour certains qui ont rencontré ces problèmes, l’expérience a été plutôt mouvementée. Cela dit, un grand nombre de correctifs ont été apportés et, plus tard dans la soirée ou tôt demain, nous aurons une nouvelle version 0.4.2.1 prête au téléchargement.

## 2) mail.i2p

Plus tôt aujourd'hui, on m'a glissé un mot de la part de postman disant qu'il avait quelques sujets qu'il voulait aborder - pour plus d'infos, consultez les journaux de la réunion (ou, si vous lisez ceci avant la réunion, passez faire un tour).

## 3) i2p-bt

L’un des inconvénients de la nouvelle version est que nous rencontrons quelques difficultés avec le portage i2p-bt. Certains des problèmes ont été identifiés, trouvés et corrigés dans la streaming lib (bibliothèque de streaming), mais un travail supplémentaire est nécessaire pour le mettre là où nous avons besoin qu’il soit.

## 4) eepsites(Sites I2P)

Depuis des mois, il y a eu des discussions sur la liste, sur le canal et sur le forum au sujet de problèmes concernant la façon dont les eepsites(I2P Sites) et l'eepproxy fonctionnent - récemment, certains ont évoqué des problèmes concernant la manière dont les en-têtes sont filtrés et lesquels le sont, d'autres ont souligné les dangers des navigateurs mal configurés, et il y a aussi la page de DrWoo qui récapitule de nombreux risques. Un événement particulièrement notable est le fait que certaines personnes travaillent activement sur des applets qui prendront le contrôle de l'ordinateur de l'utilisateur s'il ne désactive pas les applets. (DÉSACTIVEZ DONC JAVA ET JAVASCRIPT DANS VOTRE NAVIGATEUR)

Cela nous amène, bien sûr, à une discussion sur la façon dont nous pouvons sécuriser les choses. J'ai entendu des suggestions consistant à créer notre propre navigateur ou à en fournir un avec des paramètres de sécurité préconfigurés, mais soyons réalistes : c'est beaucoup plus de travail que ce à quoi quiconque ici est prêt à s'atteler. Cependant, il y a trois autres camps :

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

La première ressemble à peu près à ce que nous avons maintenant, sauf que nous filtrons le contenu rendu via quelque chose comme Muffin ou le filtre d’anonymat de Freenet. L’inconvénient ici est que cela expose encore les en-têtes HTTP, donc il nous faudrait anonymiser également la partie HTTP.

La seconde ressemble beaucoup à ce que vous pouvez voir sur `http://duck.i2p/` avec le CGIproxy, ou bien à ce que vous pouvez voir dans le fproxy de Freenet. Cela prend également en charge la partie HTTP.

La troisième a ses avantages et ses inconvénients - elle nous permet d’utiliser des interfaces bien plus attrayantes (puisque nous pouvons utiliser en toute sécurité certains JavaScript connus comme sûrs, etc), mais elle a l’inconvénient de ne pas être rétrocompatible. Peut-être une fusion de ceci avec un filtre, vous permettant d’intégrer les macros dans du html filtré ?

Quoi qu’il en soit, il s’agit d’un effort de développement important et cela aborde l’un des cas d’utilisation les plus convaincants d’I2P : des sites web interactifs sûrs et anonymes. Peut-être que quelqu’un a d’autres idées ou des informations sur la manière dont nous pourrions obtenir ce qui est nécessaire ?

## 5) ???

Ok, je suis en retard pour la réunion, alors je suppose que je devrais signer ça et l'envoyer, hein ?

=jr [voyons si j'arrive à faire fonctionner gpg correctement...]
