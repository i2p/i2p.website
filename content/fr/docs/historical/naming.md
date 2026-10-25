---
title: "Discussion sur le nommage"
description: "Débat historique sur le modèle de nommage d'I2P et pourquoi les schémas de style DNS global ont été rejetés"
slug: "naming"
aliases:
  - "/fr/docs/legacy/naming"
  - "/fr/docs/legacy/naming/"
  - "/fr/naming_discussion"
  - "/fr/naming_discussion/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

NOTE : Ce qui suit est une discussion sur les raisons qui sous-tendent le système de nommage I2P, les arguments courants et les alternatives possibles. Voir [la page de nommage](/docs/naming) pour la documentation actuelle.

## Alternatives écartées

Le nommage au sein d'I2P a été un sujet souvent débattu depuis le tout début, avec des défenseurs de toutes les possibilités du spectre. Cependant, étant donné la demande inhérente d'I2P pour une communication sécurisée et un fonctionnement décentralisé, le système de nommage traditionnel de type DNS est clairement exclu, tout comme les systèmes de vote "la majorité l'emporte".

I2P ne promeut cependant pas l'utilisation de services de type DNS, car les dégâts causés par le détournement d'un site peuvent être énormes - et les destinations non sécurisées n'ont aucune valeur. DNSsec lui-même s'appuie encore sur les registraires et les autorités de certification, alors qu'avec I2P, les requêtes envoyées vers une destination ne peuvent pas être interceptées ou la réponse usurpée, car elles sont chiffrées avec les clés publiques de la destination, et une destination elle-même n'est qu'une paire de clés publiques et un certificat. Les systèmes de type DNS d'autre part permettent à n'importe lequel des serveurs de noms sur le chemin de résolution de monter de simples attaques par déni de service et d'usurpation. L'ajout d'un certificat authentifiant les réponses comme étant signées par une autorité de certification centralisée résoudrait bon nombre des problèmes de serveurs de noms hostiles mais laisserait ouvertes les attaques par rejeu ainsi que les attaques d'autorités de certification hostiles.

Le système de nommage par vote est également dangereux, surtout compte tenu de l'efficacité des attaques Sybil dans les systèmes anonymes - l'attaquant peut simplement créer un nombre arbitrairement élevé de pairs et "voter" avec chacun pour s'emparer d'un nom donné. Les méthodes de preuve de travail peuvent être utilisées pour rendre l'identité payante, mais à mesure que le réseau grandit, la charge requise pour contacter tout le monde afin de conduire un vote en ligne devient irréaliste, ou si l'ensemble du réseau n'est pas interrogé, différents ensembles de réponses peuvent être accessibles.

Comme avec Internet cependant, I2P maintient la conception et le fonctionnement d'un système de nommage en dehors de la couche de communication (similaire à IP). La bibliothèque de nommage fournie inclut une interface simple de fournisseur de services dans laquelle les [systèmes de nommage alternatifs](#alternatives) peuvent se connecter, permettant aux utilisateurs finaux de choisir le type de compromis de nommage qu'ils préfèrent.

## Discussion

Voir aussi [Names: Decentralized, Secure, Human-Meaningful: Choose Two](https://zooko.com/distnames.html).

### Commentaires de jrandom

(adapté d'un message dans l'ancien Syndie, 26 novembre 2005)

Q : Que faire si certains hôtes ne s'accordent pas sur une adresse et si certaines adresses fonctionnent mais pas d'autres ? Qui est la source fiable d'un nom ?

R : Vous ne le faites pas. C'est en fait une différence critique entre les noms sur I2P et le fonctionnement du DNS - les noms dans I2P sont lisibles par l'homme, sécurisés, mais **pas globalement uniques**. C'est par conception, et une partie inhérente de notre besoin de sécurité.

Si je pouvais d'une manière ou d'une autre vous convaincre de changer la destination associée à un nom, je réussirais à "prendre le contrôle" du site, et en aucune circonstance cela n'est acceptable. Au lieu de cela, ce que nous faisons est de rendre les noms **uniques localement** : ils correspondent à ce que *vous* utilisez pour appeler un site, tout comme vous pouvez appeler les choses comme vous le souhaitez lorsque vous les ajoutez aux favoris de votre navigateur, ou à la liste de contacts de votre client de messagerie instantanée. Celui que vous appelez "Patron" peut être celui que quelqu'un d'autre appelle "Sally".

Les noms ne seront jamais à la fois lisibles par l'humain de manière sécurisée et globalement uniques.

### Commentaires de zzz

Ce qui suit de zzz est un examen de plusieurs plaintes courantes concernant le système de nommage d'I2P.

- **Inefficacité :** L'ensemble du fichier hosts.txt est téléchargé (s'il a changé, car eepget utilise les en-têtes etag et last-modified). Il fait environ 400K actuellement pour près de 800 hôtes.

C'est vrai, mais ce n'est pas beaucoup de trafic dans le contexte d'I2P, qui est lui-même extrêmement inefficace (bases de données floodfill, énorme surcharge de chiffrement et de remplissage, garlic routing, etc.). Si vous téléchargiez un fichier hosts.txt de quelqu'un toutes les 12 heures, cela représente en moyenne environ 10 octets/sec.

Comme c'est généralement le cas dans I2P, il y a ici un compromis fondamental entre anonymat et efficacité. Certains diraient qu'utiliser les en-têtes etag et last-modified est dangereux car cela expose quand vous avez demandé les données pour la dernière fois. D'autres ont suggéré de demander uniquement des clés spécifiques (similaire à ce que font les services de saut, mais de manière plus automatisée), possiblement au prix d'un coût supplémentaire en anonymat.

Les améliorations possibles seraient un remplacement ou un complément au carnet d'adresses (voir i2host.i2p), ou quelque chose de simple comme s'abonner à http://example.i2p/cgi-bin/recenthosts.cgi plutôt qu'à http://example.i2p/hosts.txt. Si un hypothétique recenthosts.cgi distribuait tous les hôtes des dernières 24 heures, par exemple, cela pourrait être à la fois plus efficace et plus anonyme que le hosts.txt actuel avec last-modified et etag.

Une implémentation d'exemple se trouve sur stats.i2p à l'adresse http://stats.i2p/cgi-bin/newhosts.txt. Ce script retourne un Etag avec un horodatage. Quand une requête arrive avec l'etag If-None-Match, le script retourne SEULEMENT les nouveaux hôtes depuis cet horodatage, ou 304 Not Modified s'il n'y en a aucun. De cette façon, le script retourne efficacement seulement les hôtes que l'abonné ne connaît pas, d'une manière compatible avec le carnet d'adresses.

Donc l'inefficacité n'est pas un gros problème et il existe plusieurs façons d'améliorer les choses sans changement radical.

- **Pas Évolutif :** Le fichier hosts.txt de 400K (avec recherche linéaire) n'est pas si volumineux pour le moment et nous pouvons probablement croître de 10x ou 100x avant que cela ne devienne un problème.

En ce qui concerne le trafic réseau, voir ci-dessus. Mais à moins que vous ne prévoyiez d'effectuer une requête lente en temps réel sur le réseau pour une clé, vous devez avoir l'ensemble complet des clés stockées localement, à un coût d'environ 500 octets par clé.

- **Nécessite une configuration et de la « confiance » :** Le carnet d'adresses par défaut n'est abonné qu'à http://www.i2p2.i2p/hosts.txt, qui est rarement mis à jour, ce qui entraîne une mauvaise expérience pour les nouveaux utilisateurs.

C'est tout à fait intentionnel. jrandom souhaite qu'un utilisateur "fasse confiance" à un fournisseur de hosts.txt, et comme il aime le dire, "la confiance n'est pas un booléen". L'étape de configuration tente de forcer les utilisateurs à réfléchir aux questions de confiance dans un réseau anonyme.

Comme autre exemple, la page d'erreur "I2P Site Unknown" dans le HTTP Proxy liste quelques services de saut, mais n'en "recommande" aucun en particulier, et c'est à l'utilisateur de choisir (ou non). jrandom dirait que nous faisons suffisamment confiance aux fournisseurs listés pour les répertorier mais pas assez pour aller automatiquement récupérer la clé chez eux.

Dans quelle mesure cela est-il efficace, je n'en suis pas sûr. Mais il doit y avoir une sorte de hiérarchie de confiance pour le système de nommage. Traiter tout le monde de manière égale pourrait augmenter le risque de détournement.

- **Ce n'est pas du DNS**

Malheureusement, les recherches en temps réel via I2P ralentiraient considérablement la navigation web.

De plus, le DNS est basé sur des recherches avec une mise en cache limitée et une durée de vie, tandis que les clés I2P sont permanentes.

Bien sûr, nous pourrions faire en sorte que cela fonctionne, mais pourquoi ? Ce n'est pas adapté.

- **Pas fiable :** Il dépend de serveurs spécifiques pour les abonnements de carnet d'adresses.

Oui, cela dépend de quelques serveurs que vous avez configurés. Dans I2P, les serveurs et services vont et viennent. Tout autre système centralisé (par exemple les serveurs DNS racine) aurait le même problème. Un système complètement décentralisé (où tout le monde fait autorité) est possible en implémentant une solution où "tout le monde est un serveur DNS racine", ou par quelque chose d'encore plus simple, comme un script qui ajoute tout le monde dans votre hosts.txt à votre carnet d'adresses.

Les personnes qui préconisent des solutions entièrement autoritaires n'ont généralement pas réfléchi aux problèmes de conflits et de détournement, cependant.

- **Maladroit, pas en temps réel :** C'est un assemblage disparate de fournisseurs de hosts.txt, de fournisseurs de formulaires web d'ajout de clés, de fournisseurs de services de redirection, de rapporteurs de statut de sites I2P. Les serveurs de redirection et les abonnements sont pénibles, cela devrait simplement fonctionner comme le DNS.

Voir les sections fiabilité et confiance.

Donc, en résumé, le système actuel n'est pas terriblement défaillant, inefficace ou non-évolutif, et les propositions de "simplement utiliser DNS" ne sont pas bien réfléchies.

## Alternatives

Le code source I2P contient plusieurs systèmes de nommage modulaires et prend en charge des options de configuration pour permettre l'expérimentation avec les systèmes de nommage.

- **Meta** - appelle deux systèmes de nommage ou plus dans l'ordre. Par défaut, appelle PetName puis HostsTxt.
- **PetName** - Recherche dans un fichier petnames.txt. Le format de ce fichier n'est PAS le même que hosts.txt.
- **HostsTxt** - Recherche dans les fichiers suivants, dans l'ordre :
  1. privatehosts.txt
  2. userhosts.txt
  3. hosts.txt
- **AddressDB** - Chaque hôte est listé dans un fichier séparé dans un répertoire addressDb/.
- **Eepget** - effectue une requête de recherche HTTP depuis un serveur externe - doit être empilé après la recherche HostsTxt avec Meta. Ceci pourrait augmenter ou remplacer le système de saut. Inclut la mise en cache en mémoire.
- **Exec** - appelle un programme externe pour la recherche, permet une expérimentation supplémentaire dans les schémas de recherche, indépendamment de java. Peut être utilisé après HostsTxt ou comme système de nommage unique. Inclut la mise en cache en mémoire.
- **Dummy** - utilisé comme solution de repli pour les noms Base64, échoue sinon.

Le système de nommage actuel peut être modifié avec l'option de configuration avancée `i2p.naming.impl` (redémarrage requis). Voir `core/java/src/net/i2p/client/naming` pour les détails.

Tout nouveau système devrait être empilé avec HostsTxt, ou devrait implémenter le stockage local et/ou les fonctions d'abonnement au carnet d'adresses, car le carnet d'adresses ne connaît que les fichiers hosts.txt et leur format.

## Certificats

Les destinations I2P contiennent un certificat, cependant à l'heure actuelle ce certificat est toujours null. Avec un certificat null, les destinations base64 font toujours 516 octets se terminant par "AAAA", et ceci est vérifié dans le mécanisme de fusion du carnet d'adresses, et possiblement à d'autres endroits. De plus, il n'existe aucune méthode disponible pour générer un certificat ou l'ajouter à une destination. Ces éléments devront donc être mis à jour pour implémenter les certificats.

Une utilisation possible des certificats est pour la [preuve de travail](/get-involved/todo#hashcash).

Une autre est que les "sous-domaines" (entre guillemets car il n'existe pas vraiment une telle chose, I2P utilise un système de nommage plat) soient signés par les clés du domaine de 2e niveau.

Avec toute implémentation de certificat doit venir la méthode pour vérifier les certificats. Vraisemblablement, cela se produirait dans le code de fusion du carnet d'adresses. Y a-t-il une méthode pour plusieurs types de certificats, ou plusieurs certificats ?

Ajouter un certificat authentifiant les réponses comme étant signées par une autorité de certification centralisée résoudrait de nombreux problèmes de serveurs de noms hostiles, mais laisserait ouvertes les attaques par rejeu ainsi que les attaques d'autorités de certification hostiles.
