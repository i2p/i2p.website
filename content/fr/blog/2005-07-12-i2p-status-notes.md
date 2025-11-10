---
title: "Notes de statut I2P du 2005-07-12"
date: 2005-07-12
author: "jr"
description: "Mise à jour hebdomadaire couvrant la restauration des services, l’avancement des tests SSU et l’analyse de la couche cryptographique d’I2CP en vue d’une simplification potentielle"
categories: ["status"]
---

Salut tout le monde, c’est reparti pour notre rendez-vous hebdomadaire.

* Index

1) squid/www/cvs/dev.i2p restauré 2) tests SSU 3) chiffrement I2CP 4) ???

* 1) squid/www/cvs/dev.i2p restored

Après m’être cassé la tête sur plusieurs serveurs en colocation, certains des anciens services ont été restaurés - squid.i2p (l’un des deux outproxies par défaut (mandataires sortants)), www.i2p (un pointeur sécurisé vers www.i2p.net), dev.i2p (un pointeur sécurisé vers dev.i2p.net, où se trouvent les archives des listes de diffusion, cvsweb, et les seeds netDb par défaut), et cvs.i2p (un pointeur sécurisé vers notre serveur CVS - cvs.i2p.net:2401). Mon blog est toujours porté disparu, mais son contenu avait de toute façon été perdu, donc il faudra repartir de zéro tôt ou tard. Maintenant que ces services sont de nouveau en ligne de façon fiable, il est temps de passer à la...

* 2) SSU testing

Comme mentionné dans ce petit encadré jaune sur la console du router de chacun, nous avons commencé la prochaine phase de tests sur le réseau en conditions réelles pour SSU. Ces tests ne s’adressent pas à tout le monde, mais si vous êtes aventureux et à l’aise avec un peu de configuration manuelle, consultez les détails indiqués sur votre console du router (http://localhost:7657/index.jsp). Il pourrait y avoir plusieurs séries de tests, mais je ne prévois pas de changements majeurs à SSU avant la version 0.6 (la version 0.6.1 ajoutera la prise en charge pour ceux qui ne peuvent pas rediriger leurs ports ou, plus généralement, recevoir des connexions UDP entrantes).

* 3) I2CP crypto

En retravaillant à nouveau la nouvelle documentation d'introduction, j'ai un peu de mal à justifier la couche de chiffrement supplémentaire réalisée au sein du SDK I2CP. L'objectif initial de la couche cryptographique I2CP était de fournir une protection de bout en bout de base des messages transmis, ainsi que de permettre aux clients I2CP (c.-à-d. I2PTunnel, le SAM bridge, I2Phex, azneti2p, etc.) de communiquer via des routers non fiables. À mesure que l'implémentation progressait cependant, la protection de bout en bout de la couche I2CP est devenue redondante, puisque tous les messages des clients sont chiffrés de bout en bout à l'intérieur de garlic messages (mécanisme 'garlic' d'I2P) par le router, en y joignant le leaseSet de l'expéditeur et parfois un message d'état de livraison. Cette couche garlic fournit déjà un chiffrement de bout en bout du router de l'expéditeur au router du destinataire - la seule différence étant qu'elle ne protège pas contre le fait que ce router lui-même soit hostile.

Cependant, en examinant les cas d'utilisation prévisibles, je n'arrive pas à trouver un scénario valable où le router local ne serait pas digne de confiance. Au minimum, le chiffrement I2CP ne fait que masquer le contenu du message transmis depuis le router - le router doit toujours savoir vers quelle destination il doit être envoyé. Si nécessaire, nous pouvons ajouter un écouteur I2CP SSH/SSL pour permettre au client I2CP et au router de fonctionner sur des machines distinctes, ou ceux qui en ont besoin peuvent utiliser des outils de tunnellisation existants.

Pour récapituler les couches de chiffrement utilisées actuellement, nous avons :  * La couche ElGamal/AES+SessionTag de bout en bout d'I2CP, chiffrant de    la destination de l'expéditeur à la destination du destinataire.  * La couche de garlic encryption de bout en bout du router    (ElGamal/AES+SessionTag), chiffrant du router de l'expéditeur au    router du destinataire.  * La couche de chiffrement du tunnel pour les tunnels entrants et sortants    aux sauts le long de chacun (mais pas entre l'extrémité sortante    et la passerelle entrante).  * La couche de chiffrement de transport entre chaque router.

Je souhaite rester plutôt prudent quant à la suppression de l’une de ces couches, mais je ne veux pas gaspiller nos ressources à faire un travail inutile. Ce que je propose, c’est de supprimer cette première couche de chiffrement I2CP (tout en conservant bien sûr l’authentification utilisée lors de l’établissement de la session I2CP, l’autorisation du leaseSet et l’authentification de l’expéditeur). Quelqu’un peut-il avancer une raison pour laquelle nous devrions la conserver ?

* 4) ???

C’est à peu près tout pour le moment, mais comme toujours il se passe beaucoup de choses. Toujours pas de réunion cette semaine, mais si quelqu’un a un point à aborder, n’hésitez pas à le publier sur la liste ou sur le forum. Par ailleurs, même si je lis le scrollback (historique du chat) sur #i2p, les questions ou préoccupations générales devraient plutôt être envoyées à la liste afin que davantage de personnes puissent participer à la discussion.

=jr
