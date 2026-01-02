---
title: "Enregistrements de service dans LS2"
number: "167"
author: "zzz, orignal, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "Fermé"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
toc: true
---

## Statut
Approuvé lors de la deuxième révision le 2025-04-01 ; les spécifications sont mises à jour ; pas encore implémenté.

## Vue d'ensemble

I2P n'a pas de système DNS centralisé.
Cependant, le carnet d'adresses, avec le système de noms d'hôte b32, permet
au routeur de rechercher des destinations complètes et de récupérer des ensembles de baux, qui contiennent
une liste de passerelles et de clés afin que les clients puissent se connecter à cette destination.

Ainsi, les leasesets sont quelque peu similaires à un enregistrement DNS. Mais il n'y a actuellement aucune possibilité de
savoir si cet hôte supporte des services, soit sur cette destination, soit sur une autre,
d'une manière similaire aux enregistrements DNS SRV [SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782).

La première application pour cela pourrait être le courrier électronique peer-to-peer.
Autres applications possibles : DNS, GNS, serveurs de clés, autorités de certification, serveurs de temps,
bittorrent, crypto-monnaies, autres applications peer-to-peer.

## Propositions et alternatives connexes

### Listes de services

La proposition LS2 123 [Prop123](/proposals/123-new-netdb-entries/) définissait des 'enregistrements de service' indiquant qu'une destination
participait à un service global. Les floodfills devaient agréger ces enregistrements
en 'listes de services' globales.
Cela n'a jamais été implémenté en raison de la complexité, du manque d'authentification,
des préoccupations relatives à la sécurité et au spamming.

Cette proposition diffère en ce qu'elle fournit une recherche pour un service pour une destination spécifique,
et non un pool global de destinations pour un service global.

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545) propose que chaque utilisateur exécute son propre serveur DNS.
Cette proposition est complémentaire, en ce sens que nous pourrions utiliser des enregistrements de service pour spécifier
que GNS (ou DNS) est pris en charge, avec un nom de service standard "domain" sur le port 53.

### Dot well-known

Dans [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) il est proposé que les services soient recherchés via une requête HTTP sur
/.well-known/i2pmail.key. Cela nécessite que chaque service ait un site web associé pour
héberger la clé. La plupart des utilisateurs ne gèrent pas de sites web.

Une solution de contournement est que nous pourrions supposer qu'un service pour une adresse b32 fonctionne en réalité
sur cette adresse b32. Ainsi, chercher le service pour example.i2p nécessite
la récupération HTTP depuis http://example.i2p/.well-known/i2pmail.key, mais
un service pour aaa...aaa.b32.i2p ne nécessite pas cette recherche, il peut se connecter directement.

Mais il y a une ambiguïté, car example.i2p peut également être adressée par son b32.

### Enregistrements MX

Les enregistrements SRV sont simplement une version générique des enregistrements MX pour tout service.
"_smtp._tcp" est l'enregistrement "MX".
Il n'y a pas besoin d'enregistrements MX si nous avons des enregistrements SRV, et les enregistrements MX
seuls ne fournissent pas un enregistrement générique pour tout service.

## Conception

Les enregistrements de service sont placés dans la section des options dans LS2 [LS2](/docs/specs/common-structures/).
La section des options LS2 est actuellement inutilisée.
Non supporté pour LS1.
C'est similaire à la proposition de bande passante de tunnel [Prop168](/proposals/168-tunnel-bandwidth/),
qui définit des options pour les enregistrements de construction de tunnel.

Pour rechercher une adresse de service pour un nom d'hôte ou un b32 spécifique, le routeur récupère le
leaseset et cherche l'enregistrement de service dans les propriétés.

Le service peut être hébergé sur la même destination que le LS lui-même, ou peut référencer
un nom d'hôte/b32 différent.

Si la destination cible pour le service est différente, le LS cible doit également
inclure un enregistrement de service, pointant vers lui-même, indiquant qu'il prend en charge le service.

La conception ne nécessite pas de support spécial ou de mise en cache ou de modifications dans les floodfills.
Seul l'éditeur de leaseset et le client recherchant un enregistrement de service
doivent supporter ces changements.

Des extensions mineures I2CP et SAM sont proposées pour faciliter la récupération des
enregistrements de service par les clients.

## Spécification

### Spécification des Options LS2

Les options LS2 DOIVENT être triées par clé, afin que la signature soit invariante.

Définies comme suit :

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := Le nom symbolique du service souhaité. Doit être en minuscules. Exemple : "smtp".
  Les caractères autorisés sont [a-z0-9-] et ne doivent pas commencer ou se terminer par '-'.
  Des identificateurs standard de [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) ou Linux /etc/services doivent être utilisés s'ils y sont définis.
- proto := Le protocole de transport du service souhaité. Doit être en minuscules, soit "tcp" soit "udp".
  "tcp" signifie streaming et "udp" signifie datagrammes répliables.
  Les indicateurs de protocole pour les datagrammes bruts et datagram2 peuvent être définis ultérieurement.
  Les caractères autorisés sont [a-z0-9-] et ne doivent pas commencer ou se terminer par '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priorité poids port cible [appoptions]
- ttl := durée de vie, en secondes. Entier positif. Exemple : "86400".
  Un minimum de 86400 (un jour) est recommandé, voir la section Recommandations ci-dessous pour les détails.
- priority := La priorité de l'hôte cible, plus petit est le nombre, plus il est préféré. Entier non-négatif. Exemple : "0"
  Utile uniquement s'il y a plus d'un enregistrement, mais requis même s'il n'y en a qu'un.
- weight := Un poids relatif pour les enregistrements de même priorité. Plus élevé est le nombre, plus il est probable d'être choisi. Entier non-négatif. Exemple : "0"
  Utile uniquement s'il y a plus d'un enregistrement, mais requis même s'il n'y en a qu'un.
- port := Le port I2CP sur lequel se trouve le service. Entier non-négatif. Exemple : "25"
  Le port 0 est pris en charge mais non recommandé.
- target := Le nom d'hôte ou b32 de la destination fournissant le service. Un nom d'hôte valide comme dans [NAMING](/docs/overview/naming/). Doit être en minuscules.
  Exemple : "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" ou "example.i2p".
  b32 est recommandé sauf si le nom d'hôte est "bien connu", c'est-à-dire dans les carnets d'adresses officiels ou par défaut.
- appoptions := texte arbitraire spécifique à l'application, ne doit pas contenir " " ou ",". Le codage est UTF-8.

### Exemples


Dans LS2 pour aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, pointant vers un seul serveur SMTP :

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Dans LS2 pour aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, pointant vers deux serveurs SMTP :

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

Dans LS2 pour bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, pointant vers lui-même en tant que serveur SMTP :

    "_smtp._tcp" "0 999999 25"

Format possible pour rediriger l'email (voir ci-dessous) :

    "_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"


### Limites


La structure de données de mappage utilisée pour les options LS2 limite les clés et les valeurs à 255 octets (non caractères) max.
Avec une cible b32, la optionvalue est d'environ 67 octets, donc seuls 3 enregistrements rentreraient.
Peut-être seulement un ou deux avec un champ appoptions long, ou jusqu'à quatre ou cinq avec un nom d'hôte court.
Cela devrait être suffisant ; les enregistrements multiples devraient être rares.


### Différences par rapport à [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)


- Pas de points finals
- Pas de nom après le proto
- Minuscules requises
- En format texte avec des enregistrements séparés par des virgules, et non en format DNS binaire
- Indicateurs de type d'enregistrement différents
- Champ appoptions supplémentaire


### Remarques


Aucun remplissage par caractères génériques comme (astérisque), (astérisque)._tcp, ou _tcp n'est autorisé.
Chaque service pris en charge doit avoir son propre enregistrement.

### Registre des noms de service

Les identificateurs non standards qui ne sont pas répertoriés dans [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) ou Linux /etc/services
peuvent être demandés et ajoutés à la spécification des structures communes [LS2](/docs/specs/common-structures/).

Les formats appoptions spécifiques au service peuvent également être ajoutés là-bas.

### Spécification I2CP

Le protocole [I2CP](/docs/specs/i2cp/) doit être étendu pour supporter les recherches de services.
Des codes d'erreur supplémentaires MessageStatusMessage et/ou HostReplyMessage liés à la recherche de services
sont requis.
Pour rendre la fonction de recherche générale, et pas seulement spécifique aux enregistrements de service,
la conception est de supporter la récupération de toutes les options LS2.

Implémentation : Étendre HostLookupMessage pour ajouter une demande de
options LS2 pour hash, hostname, et destination (types de demandes 2-4).
Étendre HostReplyMessage pour ajouter le mappage des options si demandé.
Étendre HostReplyMessage avec des codes d'erreur supplémentaires.

Les mappages d'options peuvent être mis en cache ou mis en cache négativement pendant une courte durée soit sur le côté client, soit du côté routeur,
dépendamment de l'implémentation. Le temps maximum recommandé est d'une heure, sauf si le TTL de l'enregistrement de service est plus court.
Les enregistrements de service peuvent être mis en cache jusqu'à la TTL spécifiée par l'application, le client, ou le routeur.

Étendre la spécification comme suit :

### Options de configuration

Ajouter ce qui suit à [I2CP-OPTIONS]

i2cp.leaseSetOption.nnn

Options à mettre dans le leaseset. Disponible uniquement pour LS2.
nnn commence à 0. La valeur de l'option contient "key=value".
(ne pas inclure les guillemets)

Exemple:

    i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p

### Message de recherche d'hôte


- Type de recherche 2 : recherche de hachage, demande de mappage d'options
- Type de recherche 3 : recherche de nom d'hôte, demande de mappage d'options
- Type de recherche 4 : recherche de destination, demande de mappage d'options

Pour le type de recherche 4, l'élément 5 est une destination.

### Message de réponse d'hôte


Pour les types de recherches 2-4, le routeur doit récupérer le leaseset,
même si la clé de recherche est dans le carnet d'adresses.

Si réussi, la réponse de l'hôte contiendra le mappage des options
du leaseset, et l'inclura en tant qu'élément 5 après la destination.
Si aucune option n'est présente dans le mappage, ou si le leaseset était en version 1,
il sera tout de même inclus en tant que mappage vide (deux octets : 0 0).
Toutes les options du leaseset seront incluses, pas seulement les options d'enregistrement de service.
Par exemple, les options pour les paramètres définis dans le futur peuvent être présentes.

En cas d'échec de la recherche du leaseset, la réponse contiendra un nouveau code d'erreur 6 (échec de la recherche du leaseset)
et n'inclura pas de mappage.
Lorsque le code d'erreur 6 est renvoyé, le champ de destination peut ou peut ne pas être présent.
Il sera présent si une recherche de nom d'hôte dans le carnet d'adresses a réussi,
ou si une recherche précédente a réussi et que le résultat était mis en cache,
ou si la destination était présente dans le message de recherche (type de recherche 4).

Si un type de recherche n'est pas pris en charge,
la réponse contiendra un nouveau code d'erreur 7 (type de recherche non pris en charge).

### Spécification SAM

Le protocole [SAMv3](/docs/api/samv3/) doit être étendu pour supporter les recherches de services.

Étendre NAMING LOOKUP comme suit :

NAMING LOOKUP NAME=example.i2p OPTIONS=true demande le mappage des options dans la réponse.

NAME peut être une destination complète en base64 lorsque OPTIONS=true.

Si la recherche de destination a réussi et que des options étaient présentes dans le leaseset,
alors dans la réponse, après la destination,
il y aura une ou plusieurs options sous la forme OPTION:key=value.
Chaque option aura un préfixe OPTION: séparé.
Toutes les options du leaseset seront incluses, pas seulement les options d'enregistrement de service.
Par exemple, les options pour les paramètres définis dans le futur peuvent être présentes.
Exemple :

    NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Les clés contenant '＝', et les clés ou valeurs contenant une nouvelle ligne,
sont considérées comme invalides et la paire clé/valeur sera supprimée de la réponse.

S'il n'y a pas d'options trouvées dans le leaseset, ou si le leaseset était en version 1,
alors la réponse n'inclura aucune option.

Si OPTIONS=true était dans la recherche, et que le leaseset n'est pas trouvé, une nouvelle valeur de résultat LEASESET_NOT_FOUND sera renvoyée.

## Alternative de recherche de nom

Une conception alternative a été envisagée, pour prendre en charge les recherches de services
comme un nom d'hôte complet, par exemple _smtp._tcp.example.i2p,
en mettant à jour [NAMING] pour spécifier la gestion des noms d'hôte commençant par '_'.
Celle-ci a été rejetée pour deux raisons :

- Des changements dans I2CP et SAM seraient encore nécessaires pour transmettre les informations TTL et port au client.
- Il ne s'agirait pas d'une fonction générale pouvant être utilisée pour récupérer d'autres options LS2
  qui pourraient être définies à l'avenir.

## Recommandations

Les serveurs doivent spécifier un TTL d'au moins 86400, et le port standard pour l'application.

## Fonctions avancées

### Recherches récursives

Il peut être souhaitable de prendre en charge les recherches récursives, où chaque leaseset successif
est vérifié pour un enregistrement de service pointant vers un autre leaseset, à la manière DNS.
Cela n'est probablement pas nécessaire, au moins dans une implémentation initiale.

TODO

### Champs spécifiques à l'application

Il peut être souhaitable d'avoir des données spécifiques à l'application dans l'enregistrement de service.
Par exemple, l'opérateur de example.i2p peut souhaiter indiquer que le courrier électronique doit
être acheminé vers example@mail.i2p. La partie "example@" devrait être dans un champ séparé
de l'enregistrement de service, ou retirée de la cible.

Même si l'opérateur gère son propre service de messagerie, il peut souhaiter indiquer que
le courrier électronique doit être envoyé à example@example.i2p. La plupart des services I2P sont gérés par une seule personne.
Ainsi, un champ distinct peut également être utile ici.

TODO comment faire cela de manière générique

### Changements nécessaires pour l'email

Hors du champ de cette proposition. Voir [DOTWELLKNOWN] pour une discussion.

## Notes d'implémentation

La mise en cache des enregistrements de service jusqu'à la TTL peut être effectuée par le routeur ou l'application,
dépendamment de l'implémentation. Le choix de mettre en cache de manière persistante est également dépendant de l'implémentation.

Les recherches doivent également chercher le leaseset cible et vérifier qu'il contient un enregistrement "self"
avant de renvoyer la destination cible au client.

## Analyse de sécurité

Comme le leaseset est signé, tous les enregistrements de service à l'intérieur sont authentifiés par la clé de signature de la destination.

Les enregistrements de service sont publics et visibles par les floodfills, à moins que le leaseset ne soit chiffré.
Tout routeur demandant le leaseset pourra voir les enregistrements de service.

Un enregistrement SRV autre que "self" (c'est-à-dire un qui pointe vers un autre nom d'hôte/cible b32)
ne nécessite pas le consentement du nom d'hôte/cible b32 ciblé.
Il n'est pas clair si une redirection d'un service vers une destination arbitraire pourrait faciliter une sorte
d'attaque, ou quel serait le but d'une telle attaque.
Cependant, cette proposition atténue une telle attaque en exigeant que la cible
publie également un enregistrement SRV "self". Les implémenteurs doivent rechercher un enregistrement "self"
dans le leaseset de la cible.

## Compatibilité

LS2: Pas de problèmes. Toutes les implémentations connues actuellement ignorent le champ des options dans LS2,
et sautent correctement un champ des options non vide.
Ceci a été vérifié lors des tests par Java I2P et i2pd pendant le développement de LS2.
LS2 a été implémenté dans 0.9.38 en 2016 et est bien supporté par toutes les implémentations de routeur.
La conception ne nécessite pas de support spécial ou de mise en cache ou de modifications dans les floodfills.

Naming: '_' n'est pas un caractère valide dans les noms d'hôte i2p.

I2CP: Les types de recherche 2-4 ne doivent pas être envoyés à des routeurs en dessous de la version API minimum
à laquelle elle est prise en charge (à déterminer).

SAM: Le serveur SAM Java ignore les clés/valeurs supplémentaires telles que OPTIONS=true.
i2pd devrait également, à vérifier.
Les clients SAM ne recevront pas les valeurs supplémentaires dans la réponse, sauf demandées avec OPTIONS=true.
Aucun changement de version ne devrait être nécessaire.

