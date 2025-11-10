---
title: "Rencontrez votre mainteneur: DivaExchange"
date: 2022-09-26
author: "sadie"
description: "Une conversation avec DivaExchange"
categories: ["general"]
API_Translate: vrai
---

*Dans ce deuxième épisode de Meet Your Maintainer, j’ai contacté Konrad de DIVA.EXCHANGE pour parler de la recherche et des services de DIVA. DIVA.EXCHANGE développe des logiciels dans le but de fournir une technologie bancaire libre pour tous. Elle est sécurisée sans infrastructure centrale et repose sur les technologies blockchain et I2P.*

**Qu'est-ce qui vous a amené à vous intéresser à I2P ?**

Il y a environ dix ans, j’ai fait une présentation pour "Technologieforum Zug" - un réseau technologique très local destiné aux professionnels du monde de l’entreprise. Je leur présentais I2P et Tor en tant que overlay networks (réseaux superposés) - pour leur montrer qu’il existe ailleurs d’autres choses intéressantes.

J’ai toujours eu un vif intérêt pour les technologies liées à la cryptographie. De manière générale, je peux dire que mes centres d’intérêt principaux étaient et sont toujours : les réseaux, la liberté et la vie privée tant sur le plan technique que social, des algorithmes intéressants, comme HashCash entre 2000 et 2010, qui était un algorithme de preuve de travail très efficace créé dans des universités au Royaume-Uni à la fin des années 1990.

I2P m’a fasciné parce qu’il est vraiment soigneusement conçu — de l’architecture jusqu’à l’implémentation en Java et C++. Personnellement, je préfère des programmes découplés et de petite taille qui ne font qu’une seule chose. J’ai donc été plutôt séduit par la version C++, I2Pd, qui est sobre, rapide et sans dépendances. Il fonctionne très bien pour moi.

**Quelles qualités, sur le plan de ses capacités techniques, correspondaient à votre propre travail ou à vos centres d’intérêt ?**

J'adore l'artisanat. C'est de l'art. Et I2P, c'est de l'artisanat moderne. I2P crée, pour les utilisateurs finaux, des valeurs qui ne s'achètent pas : autonomie, liberté et sérénité.

I2P me fascine parce qu'il est agnostique. N'importe qui peut exécuter à peu près n'importe quoi sur I2P tant que cela parle TCP ou UDP - et peut gérer une certaine latence. En réalité : "le réseau est l'ordinateur" et la communication est véritablement privée selon l'état actuel des connaissances.

**À qui s'adresse DIVA ?**

DIVA fait l’objet d’un développement actif ; le projet s’adresse donc aux chercheurs, aux développeurs de logiciels, aux professionnels de la communication (rédacteurs, illustrateurs…) et aux personnes qui souhaitent apprendre des concepts réellement nouveaux dans le domaine des technologies distribuées.

Une fois que DIVA aura mûri - s'il vous plaît, ne me demandez pas quand - DIVA sera une banque entièrement distribuée, auto-hébergée, pour tout le monde.

**Pouvez-vous me parler de ce que fait DIVA ?**

Comme déjà dit, DIVA sera une banque entièrement distribuée et auto-hébergée, pour tous. "Banking" signifie : épargne, paiements, investissements, prêts - donc tout ce que tout le monde fait au quotidien. Veuillez noter dans ce contexte : DIVA fonctionne sans aucune infrastructure centrale et DIVA ne sera jamais - tant que j'aurai mon mot à dire - une crypto-monnaie ni un jeton. Il ne peut y avoir aucun modèle économique central impliqué. Si une transaction génère des frais parce qu'un nœud de l'infrastructure distribuée a effectué un travail, alors ces frais reviennent au nœud qui a effectué le travail.

Pourquoi une « banque » ? Parce que la liberté et l’autonomie financières sont essentielles pour mener une vie bonne et paisible et pour pouvoir prendre, en toute liberté, toutes ces décisions quotidiennes, petites comme grandes. Par conséquent, les personnes doivent posséder leurs petits composants technologiques sécurisés afin de faire tout ce qu’elles veulent sans être influencées.

Eh bien, dites bonjour à DIVA, qui s’appuie sur I2P.

**Quels sont vos prochains objectifs ? Quels sont vos objectifs ambitieux ?**

Il y a un objectif immédiat : comprendre l’impact de SSU2, récemment implémenté dans I2P. C’est un objectif technique pour les prochaines semaines.

Puis, probablement cette année : quelques transactions en cryptomonnaie utilisant DIVA sur des réseaux de test. N'oubliez pas : DIVA est un projet de recherche et les personnes doivent être encouragées à faire leurs propres projets avec DIVA - de la manière qui leur convient. Nous n'exploitons aucune infrastructure ou assimilé pour d'autres, à l'exception de quelques réseaux de test transparents, afin d'accroître le savoir et la compréhension de tous. Il est recommandé de rester en contact avec DIVA via les réseaux sociaux ([@DigitalValueX](http://twitter.com/@DigitalValueX)) ou des salons de discussion afin de trouver l'inspiration sur ce qu'il est possible de faire avec DIVA.

Je souhaite également aborder un point important pour la communauté I2P : DIVA est basée sur divachain - qui est elle-même basée sur I2P. Divachain est une couche de stockage entièrement distribuée, très générique. Ainsi, à titre d’exemple : si un développeur I2P estime qu’un DNS « trustless » (sans nécessité de faire confiance à un tiers) entièrement distribué serait une excellente idée - eh bien, voilà un autre cas d’utilisation de divachain. Entièrement distribué - aucune confiance nécessaire - le tout anonyme.

**De quels autres services et contributions êtes-vous responsable ?**

DIVA.EXCHANGE - qui est l'association ouverte qui développe DIVA - exploite un reseed server (serveur de réensemencement) pour I2P depuis quelques années. Il est donc probable que presque tous les utilisateurs d'I2P ont été en contact avec nous d'une manière ou d'une autre par le passé. Petite précision : le reseed server DIVA.EXCHANGE est également disponible en tant que service .onion - ainsi, I2P bootstrapping (amorçage I2P) peut être effectué via le réseau Tor - ce qui constitue, au moins de mon point de vue, une couche de protection supplémentaire au moment d'entrer sur le réseau.

DIVA a également créé une bibliothèque I2P SAM. Ainsi, les développeurs peuvent créer n'importe quelle application moderne basée sur I2P. Elle est sur github et devient de plus en plus populaire : [github.com/diva-exchange/i2p-sam/](http://github.com/diva-exchange/i2p-sam/). Elle est complète, bien documentée et offre de nombreux exemples.

**Quelles priorités, selon vous, toute personne souhaitant contribuer au réseau I2P devrait-elle prendre en compte ?**

Lancez votre nœud I2P. Découvrez les différentes variantes, comme les versions Docker d’I2Pd, ou d’autres installations disponibles pour plusieurs systèmes d’exploitation. Plusieurs variantes sont disponibles et il est important d’être à l’aise avec l’installation et la configuration locales.

Alors : pensez à vos compétences - en réseaux, en programmation, en communication ? I2P propose de nombreux défis intéressants : les personnes ayant des compétences en réseaux pourraient vouloir exploiter un reseed server (serveur de réensemencement) - ils sont très importants pour le réseau. Les programmeurs peuvent contribuer à la version Go, C++ ou Java d'I2P. Et les communicants sont toujours nécessaires : parler d'I2P d'un point de vue objectif et réaliste aide beaucoup. Chaque contribution, même modeste, est la bienvenue.

Dernier point, mais non des moindres: si vous êtes chercheur ou étudiant - veuillez nous contacter chez DIVA.EXCHANGE ou auprès de l'équipe I2P - les travaux de recherche sont importants pour I2P.

**Selon vous, où en sont aujourd’hui la discussion et les perspectives autour d’outils comme I2P ?**

Je dois probablement dire quelque chose à propos des perspectives: I2P est important pour tout le monde. J’espère que la communauté I2P - développeurs, communicants, etc. - reste motivée par les rares qui apprécient profondément leur travail acharné sur une technologie véritablement exigeante.

J'espère que de plus en plus de développeurs verront l'intérêt à développer des logiciels basés sur I2P. Car cela créerait davantage de cas d'utilisation pour les utilisateurs finaux.

**Pouvez-vous me parler un peu de votre propre flux de travail I2P ? Quels sont vos propres cas d'utilisation ?**

Je suis développeur, testeur et chercheur. J’ai donc besoin de tout mettre dans des conteneurs pour rester flexible. I2Pd s’exécute dans 1..n conteneurs sur plusieurs systèmes pour fournir des services tels que : répondre aux requêtes de reseed (réamorçage de la netDb), servir le site de test diva.i2p, exécuter des parties du réseau de test I2P DIVA - voir testnet.diva.exchange, et j’ai aussi des conteneurs pour servir mes navigateurs locaux en tant que proxy combiné I2P et Tor.

**Comment la communauté I2P peut-elle soutenir votre travail ?**

Nous sommes présents sur les réseaux sociaux, comme [@DigitalValueX](http://twitter.com/@DigitalValueX) - alors suivez-nous là-bas. De plus, nous serions ravis de voir encore davantage d’implication sur [github.com/diva-exchange](http://github.com/diva-exchange) - il a déjà suscité de plus en plus d’attention ces derniers mois. Merci beaucoup pour cela !
