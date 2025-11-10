---
title: "Notes de statut d'I2P pour le 2006-10-03"
date: 2006-10-03
author: "jr"
description: "Analyse des performances du réseau, investigation des goulots d’étranglement du processeur, planification de la sortie de Syndie 1.0, et évaluation de la gestion de versions distribuée"
categories: ["status"]
---

Salut à tous, des notes de statut en retard cette semaine

* Index

1) État du réseau 2) État du développement du Router 3) Justification de Syndie (suite) 4) État du développement de Syndie 5) Contrôle de version distribué 6) ???

* 1) Net status

Les une à deux dernières semaines ont été assez stables sur irc et d'autres services, bien que dev.i2p/squid.i2p/www.i2p/cvs.i2p aient connu quelques accrocs (en raison de problèmes temporaires liés au système d'exploitation). La situation semble stable pour le moment.

* 2) Router dev status

L'autre facette de la discussion sur Syndie est "alors, qu'est-ce que cela signifie pour le router ?", et pour y répondre, laissez-moi expliquer brièvement où en est le développement du router à l'heure actuelle.

Dans l’ensemble, ce qui empêche le router d’atteindre la version 1.0, à mon avis, ce sont ses performances, et non ses propriétés d’anonymat. Certes, il y a des aspects liés à l’anonymat à améliorer, mais même si nous obtenons de très bonnes performances pour un réseau anonyme, nos performances ne sont pas suffisantes pour une utilisation plus large. De plus, des améliorations de l’anonymat du réseau n’en amélioreront pas les performances (dans la plupart des cas qui me viennent à l’esprit, les améliorations de l’anonymat réduisent le débit et augmentent la latence). Nous devons d’abord résoudre les problèmes de performances, car si les performances sont insuffisantes, l’ensemble du système est insuffisant, quelle que soit la robustesse de ses techniques d’anonymat.

Alors, qu’est-ce qui freine nos performances ? Étrangement, cela semble être notre utilisation du CPU. Avant d’expliquer exactement pourquoi, un peu plus de contexte d’abord.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

Par conséquent, nous avons besoin de niveaux de routers - certains accessibles mondialement avec des limites de bande passante élevées (tier A), d’autres non (tier B). Cela a déjà, en pratique, été mis en œuvre via les informations de capacité dans la netDb, et il y a un jour ou deux, le rapport de tier B à tier A était d’environ 3 pour 1 (93 routers de cap L, M, N ou O, et 278 de cap K).

À présent, il y a essentiellement deux ressources rares à gérer au niveau A : la bande passante et le CPU. On peut gérer la bande passante par les moyens habituels (répartir la charge sur un vaste pool, faire en sorte que certains pairs absorbent des quantités énormes [par ex. ceux en T3], et rejeter ou limiter le débit de tunnels ou de connexions individuellement).

Gérer l'utilisation du CPU est plus difficile. Le principal goulot d’étranglement du CPU observé sur les routers de niveau A est le déchiffrement des requêtes de construction de tunnel. Les routers de grande taille peuvent être (et sont) entièrement accaparés par cette activité — par exemple, sur l’un de mes routers, le temps moyen de déchiffrement d’un tunnel sur l’ensemble de sa durée de vie est de 225 ms, et la fréquence *moyenne* sur l’ensemble de la durée de vie d’un déchiffrement de requête de tunnel est de 254 événements par 60 secondes, soit 4,2 par seconde. En multipliant simplement ces deux valeurs, on constate que 95 % du CPU est consommé par le seul déchiffrement des requêtes de tunnel (et cela ne tient pas compte des pics dans le nombre d’événements). Ce router parvient quand même à participer à 4-6000 tunnels simultanément, en acceptant environ 80 % des requêtes déchiffrées.

Malheureusement, comme le CPU de ce router est très fortement sollicité, il doit rejeter un nombre significatif de demandes de construction de tunnel avant même qu'elles puissent être déchiffrées (sinon les demandes resteraient dans la file d'attente si longtemps que, même si elles étaient acceptées, le demandeur initial les aurait considérées comme perdues ou la charge aurait été trop élevée pour faire quoi que ce soit de toute façon). Dans cette optique, le taux d'acceptation de 80% du router paraît bien pire - sur toute sa durée de vie, il a déchiffré environ 250k demandes (ce qui signifie qu'environ 200k ont été acceptées), mais il a dû rejeter environ 430k demandes dans la file d'attente de déchiffrement en raison d'une surcharge du CPU (transformant ce taux d'acceptation de 80% en 30%).

Les solutions semblent aller dans le sens de la réduction du coût CPU associé au déchiffrement des requêtes de tunnel. Si nous réduisons le temps CPU d’un ordre de grandeur, cela augmenterait sensiblement la capacité du router de niveau A, réduisant ainsi les refus (à la fois explicites et implicites, dus aux requêtes abandonnées). Cela augmenterait à son tour le taux de réussite de la construction des tunnels, réduisant ainsi la fréquence des expirations de lease, ce qui réduirait ensuite la charge de bande passante sur le réseau due à la reconstruction des tunnels.

Une méthode pour y parvenir serait de modifier les requêtes de construction de tunnel en passant de l’Elgamal en 2048 bits à, disons, 1024 ou 768 bits. Le problème, toutefois, est que si vous cassez le chiffrement d’un message de requête de construction de tunnel, vous connaissez le chemin complet du tunnel. Même si nous empruntions cette voie, qu’est-ce que cela nous apporterait ? Une amélioration d’un ordre de grandeur du temps de déchiffrement pourrait être annulée par une augmentation d’un ordre de grandeur du rapport de tier B à tier A (également appelé le problème des passagers clandestins), et nous serions alors coincés, puisqu’il n’y a aucun moyen de passer à l’Elgamal en 512 ou 256 bits (et nous regarder dans le miroir ;)

Une alternative consisterait à recourir à une cryptographie plus faible mais à supprimer la protection contre les attaques par comptage de paquets que nous avons ajoutée avec le nouveau processus de construction de tunnel. Cela nous permettrait d'utiliser des clés négociées entièrement éphémères dans un tunnel télescopique de type Tor (ce qui, encore une fois, exposerait le créateur du tunnel à des attaques passives triviales de comptage de paquets qui permettent d'identifier un service).

Une autre idée est de publier et d’utiliser des informations de charge encore plus explicites dans le netDb, permettant aux clients de détecter plus précisément des situations comme celle ci-dessus où un router à haut débit rejette 60 % de ses messages de requête de tunnel sans même les examiner. Il y a quelques expériences qui valent la peine d’être menées dans cette voie, et elles peuvent être réalisées avec une rétrocompatibilité totale, nous devrions donc les voir apparaître bientôt.

Donc, c'est le goulot d'étranglement dans le router/réseau tel que je le vois aujourd'hui. Toutes les suggestions sur la manière dont nous pouvons y remédier seraient très appréciées.

* 3) Syndie rationale continued

Il y a un message substantiel sur le forum à propos de Syndie et de la place qu’elle occupe par rapport au reste - allez le consulter à l’adresse <http://forum.i2p.net/viewtopic.php?t=1910>

Par ailleurs, j'aimerais simplement mettre en avant deux extraits de la documentation de Syndie en cours d'élaboration. Tout d'abord, tiré d'irc (et de la FAQ pas encore publiée):

<bar> une question que je me pose, c'est: qui, plus tard, aura        assez de cran pour héberger des serveurs/archives de production syndie ?  <bar> ne seront-elles pas aussi faciles à repérer que les eepsites(I2P Sites)        le sont aujourd'hui ?  <jrandom> les archives syndie publiques n'ont pas la capacité de        *lire* le contenu publié sur les forums, à moins que les forums ne publient        les clés nécessaires pour le faire  <jrandom> et voir le deuxième paragraphe de usecases.html  <jrandom> bien sûr, ceux qui hébergent des archives et reçoivent des        ordres légaux de retirer un forum le feront probablement  <jrandom> (mais alors les gens peuvent déménager vers une autre        archive, sans perturber le fonctionnement du forum)  <void> ouais, tu devrais mentionner le fait que la migration vers un        autre support va être transparente  <bar> si mon archive ferme, je peux téléverser tout mon forum sur une        nouvelle, non ?  <jrandom> exactement, bar  <void> ils peuvent utiliser deux méthodes en même temps pendant la migration  <void> et n'importe qui est capable de synchroniser les supports  <jrandom> exact, void

La section pertinente du (pas encore publié) Syndie usecases.html est:

Bien que de nombreux groupes souhaitent souvent organiser des discussions dans   un forum en ligne, la nature centralisée des forums traditionnels   (sites web, BBS, etc) peut poser problème. Par exemple, le site   hébergeant le forum peut être mis hors ligne par des attaques par déni de service   ou à la suite d’une mesure administrative. De plus, le serveur unique   offre un point simple pour surveiller l’activité du groupe, de sorte que même   si un forum est pseudonyme, ces pseudonymes peuvent être associés à l’adresse IP   qui a publié ou lu des messages individuels.

De plus, non seulement les forums sont décentralisés, mais ils sont organisés de manière ad hoc tout en restant pleinement compatibles avec d'autres techniques d'organisation. Cela signifie qu'un petit groupe de personnes peut gérer son forum en utilisant une technique (en publiant ses messages sur un site wiki), un autre peut gérer son forum en utilisant une autre technique (en publiant ses messages dans une table de hachage distribuée comme OpenDHT), et si une personne connaît les deux techniques, elle peut synchroniser les deux forums entre eux. Cela permet aux personnes qui ne connaissaient que le site wiki de parler à celles qui ne connaissaient que le service OpenDHT, sans rien savoir les unes des autres. Plus largement, Syndie permet à des cellules individuelles de contrôler leur propre exposition tout en communiquant à l'échelle de l'ensemble de l'organisation.

* 4) Syndie dev status

Il y a eu beaucoup de progrès sur Syndie ces derniers temps, avec 7 versions alpha distribuées aux gens sur le canal IRC. La plupart des problèmes majeurs de l’interface scriptable ont été traités, et j’espère que nous pourrons publier la version 1.0 de Syndie plus tard ce mois-ci.

Est-ce que je viens de dire "1.0" ? Et comment ! Bien que Syndie 1.0 soit une application en mode texte, et qu’elle ne soit même pas comparable, en termes d’ergonomie, à d’autres applications en mode texte (comme mutt ou tin), elle offrira l’ensemble des fonctionnalités, permettra des stratégies de syndication via HTTP et basées sur des fichiers, et, espérons-le, démontrera aux développeurs potentiels les capacités de Syndie.

Pour l’instant, je prévois provisoirement une version Syndie 1.1 (permettant aux utilisateurs d’organiser plus efficacement leurs archives et leurs habitudes de lecture) et peut-être une version 1.2 pour intégrer des fonctionnalités de recherche (à la fois des recherches simples et, peut-être, les recherches en texte intégral de Lucene). Syndie 2.0 sera probablement la première version avec interface graphique (GUI), avec le module d’extension pour navigateur prévu pour la 3.0. La prise en charge d’archives supplémentaires et de réseaux de distribution de messages arrivera lorsqu’ils seront implémentés, bien sûr (freenet, mixminion/mixmaster/smtp, opendht, gnutella, etc).

Je me rends toutefois compte que Syndie 1.0 ne sera pas la révolution que certains souhaitent, car les applications en mode texte sont vraiment destinées aux geeks, mais j’aimerais essayer de nous défaire de l’habitude de considérer "1.0" comme une version finale et de la voir plutôt comme un début.

* 5) Distributed version control

Jusqu'à présent, je bricolais avec subversion comme VCS (système de contrôle de versions) pour Syndie, même si je ne suis vraiment à l'aise qu'avec CVS et clearcase. C'est parce que je suis hors ligne la plupart du temps, et même quand je suis en ligne, le dial-up (accès commuté) est lent, donc les diff/revert/etc locaux de subversion m'ont été bien utiles. Cependant, hier, void m'a soufflé l'idée que nous devrions plutôt nous pencher sur l'un des systèmes distribués.

Je les ai examinés il y a quelques années lorsque j’évaluais un VCS (système de gestion de versions) pour I2P, mais je les ai écartés parce que je n’avais pas besoin de leurs fonctionnalités hors ligne (j’avais alors un bon accès à Internet), donc apprendre à les utiliser ne valait pas la peine. Ce n’est plus le cas, donc je m’y intéresse un peu plus maintenant.

- From what I can see, darcs, monotone, and codeville are the top

Parmi les candidats, le VCS (système de contrôle de versions) basé sur des patches de darcs semble particulièrement attrayant. Par exemple, je peux faire tout mon travail en local et simplement envoyer via scp les diffs gzip'ed & gpg'ed vers un répertoire apache sur dev.i2p.net, et les gens peuvent contribuer leurs propres modifications en publiant leurs diffs gzip'ed et gpg'ed aux emplacements de leur choix. Quand vient le moment de taguer une version, je ferais un darcs diff qui précise l’ensemble des patches contenus dans la version et je pousserais ce diff .gz'ed/.gpg'ed comme les autres (ainsi que je publierais de vrais fichiers tar.bz2, .exe et .zip, bien sûr ;)

Et, fait particulièrement intéressant, ces diffs gzip/gpg peuvent être publiés comme pièces jointes aux messages Syndie, permettant à Syndie de s’auto-héberger.

Quelqu’un a de l’expérience avec ces trucs-là ? Des conseils ?

* 6) ???

Seulement 24 écrans pleins de texte cette fois (y compris le message sur le forum) ;) Je n'ai malheureusement pas pu assister à la réunion, mais comme toujours, j'aimerais beaucoup vous lire si vous avez des idées ou des suggestions - il vous suffit de poster sur la liste, sur le forum, ou de passer sur IRC.

=jr
