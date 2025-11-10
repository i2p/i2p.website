---
title: "Notes d'état d'I2P du 2006-09-12"
date: 2006-09-12
author: "jr"
description: "Sortie de la version 0.6.1.25 avec des améliorations de la stabilité du réseau, des optimisations d'I2PSnark et une refonte complète de Syndie avec des forums distribués hors ligne"
categories: ["status"]
---

Salut à tous, voici nos *tousse* notes d’avancement hebdomadaires

* Index:

1) 0.6.1.25 et état du réseau 2) I2PSnark 3) Syndie (quoi/pourquoi/quand) 4) Questions de cryptographie de Syndie 5) ???

* 1) 0.6.1.25 and net status

L’autre jour, nous avons publié la version 0.6.1.25, comprenant la multitude de corrections de bogues accumulées au cours du mois écoulé, ainsi que le travail de zzz sur I2PSnark et celui de Complication visant à rendre notre code de synchronisation de l’heure un peu plus robuste. En ce moment, le réseau semble assez stable, même si IRC a été un peu chahuté ces derniers jours (pour des raisons sans rapport avec I2P). Avec peut‑être la moitié du réseau mise à niveau vers la dernière version, les taux de réussite de construction de tunnel n’ont pas beaucoup changé, mais le débit global semble avoir augmenté (probablement en raison d’une augmentation du nombre de personnes utilisant I2PSnark).

* 2) I2PSnark

Les mises à jour de zzz pour I2PSnark incluaient des optimisations de protocole ainsi que des modifications des interfaces web, comme décrit dans le journal des modifications [1]. Il y a également eu quelques petites mises à jour pour I2PSnark depuis la version 0.6.1.25, et peut-être que zzz pourra nous donner un aperçu de la situation lors de la réunion de ce soir.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

Comme vous le savez tous, je me consacre à la refonte de Syndie, même si "refonte" n’est peut-être pas le terme adéquat. Vous pouvez peut-être considérer ce qui est actuellement déployé comme une "preuve de concept", puisque le nouveau Syndie a été repensé et réimplémenté à partir de zéro, même si de nombreux concepts demeurent. Lorsque je fais référence à Syndie ci-dessous, je parle du nouveau Syndie.

* 3.1) What is Syndie

Syndie est, à son niveau le plus élémentaire, un système permettant d'exploiter des forums distribués hors ligne. Bien que sa structure permette un grand nombre de configurations différentes, la plupart des besoins seront satisfaits en sélectionnant l'une des options pour chacun des trois critères suivants:  - Types de forum:    - Auteur unique (blog typique)    - Auteurs multiples (blog multi-auteurs)**    - Ouvert (groupes de discussion, bien que des restrictions puissent être incluses de sorte que seuls      les utilisateurs autorisés** puissent publier de nouveaux sujets, tandis que n'importe qui peut commenter      ces nouveaux sujets)  - Visibilité:    - Tout le monde peut tout lire    - Seules les personnes autorisées* peuvent lire les messages, mais certaines métadonnées sont exposées    - Seules les personnes autorisées* peuvent lire les messages, ou même savoir qui publie    - Seules les personnes autorisées* peuvent lire les messages, et personne ne sait qui      publie  - Commentaires/réponses:    - N'importe qui peut commenter ou envoyer des réponses privées à l'auteur/      propriétaire du forum    - Seules les personnes autorisées** peuvent commenter, et n'importe qui peut envoyer des réponses      privées    - Personne ne peut commenter, mais n'importe qui peut envoyer des réponses privées    - Personne ne peut commenter, et personne ne peut envoyer des réponses privées

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** L'autorisation de publier, de mettre à jour et/ou de commenter est accordée en fournissant à ces utilisateurs des clés privées asymétriques avec lesquelles signer les messages, la clé publique correspondante étant incluse dans les métadonnées du forum en tant qu'autorisée à publier, gérer ou commenter sur le forum.  Autrement, les clés publiques de signature des utilisateurs autorisés individuellement peuvent être répertoriées dans les métadonnées.

Chaque message peut contenir de nombreux éléments différents :  - N'importe quel nombre de pages, avec pour chaque page des données hors bande précisant    le type de contenu, la langue, etc.  Tout formatage peut être utilisé, puisqu'il    revient à l'application cliente d'afficher le contenu en toute sécurité - le texte brut    doit être pris en charge, et les clients qui le peuvent devraient prendre en charge HTML.  - N'importe quel nombre de pièces jointes (là encore, avec des données hors bande décrivant la    pièce jointe)  - Un petit avatar pour le message (mais s'il n'est pas spécifié, l'avatar    par défaut de l'auteur est utilisé)  - Un ensemble de références à d'autres messages, forums, archives, URL, etc (qui    peuvent inclure les clés nécessaires pour publier, gérer, ou lire les forums    référencés)

Dans l'ensemble, Syndie fonctionne au niveau de la *couche de contenu* - les messages individuels sont contenus dans des fichiers zip chiffrés, et participer au forum signifie simplement partager ces fichiers. Il n'y a aucune dépendance quant à la manière dont les fichiers sont transférés (via I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email), mais de simples outils d'agrégation et de distribution seront fournis avec la version standard de Syndie.

L’interaction avec le contenu de Syndie se fera de plusieurs façons. Tout d’abord, il existe une interface en mode texte scriptable, permettant, via la ligne de commande ou de manière interactive, d’effectuer les opérations de base consistant à lire, écrire, gérer et synchroniser les forums. Par exemple, voici un simple script pour générer une nouvelle publication "message du jour" -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

Il suffit de rediriger cela via un pipe vers l’exécutable syndie et le tour est joué : cat motd-script | ./syndie > syndie.log

De plus, des travaux sont en cours pour une interface graphique de Syndie, qui inclut le rendu sécurisé de pages en texte brut et en HTML (bien sûr, avec la prise en charge d’une intégration transparente avec les fonctionnalités de Syndie).

Les applications basées sur l'ancien code "sucker" de Syndie permettront l'aspiration et la réécriture de pages et sites web classiques, afin qu'ils puissent être utilisés comme des billets Syndie à une ou plusieurs pages, y compris des images et d'autres ressources en pièces jointes.

À terme, des plugins firefox/mozilla sont prévus pour détecter et importer les fichiers au format Syndie et les références Syndie, ainsi que pour notifier l’interface graphique locale de Syndie qu’un forum, un sujet, un tag (étiquette), un auteur ou un résultat de recherche particulier doit être mis au premier plan.

Bien sûr, puisque Syndie est, au fond, une couche de contenu dotée d'un format de fichier défini et d'algorithmes cryptographiques, d'autres applications ou des implémentations alternatives verront probablement le jour au fil du temps.

* 3.2) Why does Syndie matter?

Au cours des derniers mois, j'ai entendu plusieurs personnes demander pourquoi je travaille sur un outil de forum/blog - qu'est-ce que cela a à voir avec la fourniture d'un anonymat fort ?

La réponse: *tout*.

Pour résumer brièvement :  - La conception de Syndie, en tant qu’application cliente sensible aux exigences d’anonymat, évite soigneusement les problèmes complexes de sensibilité des données que presque toutes les applications non conçues avec l’anonymat à l’esprit n’évitent pas.  - En opérant au niveau de la couche de contenu, Syndie ne dépend ni des performances ni de la fiabilité de réseaux distribués comme I2P, Tor ou Freenet, bien qu’elle puisse en tirer parti lorsque c’est approprié.  - Ce faisant, elle peut fonctionner pleinement avec de petits mécanismes ad hoc de distribution de contenu - des mécanismes qui peuvent ne pas valoir l’effort, pour des adversaires puissants, d’être contrecarrés (puisque le 'payoff' de compromettre seulement quelques dizaines de personnes dépassera probablement le coût de la mise en œuvre des attaques)  - Cela implique que Syndie sera utile même sans quelques millions de personnes l’utilisant - de petits groupes sans lien entre eux devraient mettre en place leur propre schéma privé de distribution Syndie sans nécessiter la moindre interaction avec d’autres groupes, ni même que ces groupes en aient connaissance.  - Puisque Syndie ne repose pas sur l’interaction en temps réel, elle peut même utiliser des systèmes et des techniques d’anonymat à haute latence pour éviter les attaques auxquelles tous les systèmes à faible latence sont vulnérables (telles que les attaques d’intersection passives, les attaques temporelles passives et actives, et les attaques de mélange actives).

On the whole, its my view that Syndie is even more important to I2P's core mission (providing strong anonymity to those who need it) than even the router. Its not the end-all, be-all, but its a key step.

* 3.3) When can we use Syndie?

Bien qu'une grande partie du travail ait été accomplie (y compris presque toute l'interface texte et une bonne partie de l'interface graphique), il reste encore du travail à faire. La première version de Syndie inclura les fonctionnalités de base suivantes :

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

Le critère que j’utiliserai pour le publier sera "entièrement fonctionnel". Monsieur Tout-le-monde ne va pas s’embêter avec une application en mode texte, mais j’espère que quelques geeks s’y mettront.

Les versions ultérieures amélioreront les capacités de Syndie sur plusieurs axes :  - Interface utilisateur :   - Interface graphique basée sur SWT   - Extensions pour navigateur Web   - Interface texte par scraping Web (récupération et réécriture des pages)   - Interface de lecture IMAP/POP3/NNTP  - Prise en charge du contenu   - Texte brut   - HTML (rendu sécurisé dans l’interface graphique, pas dans un navigateur)   - BBCode (?)  - Syndication   - Feedspace, Feedtree et autres outils de synchronisation à faible latence   - Freenet (stockage des fichiers .snd aux CHK@s et archives référençant
    les fichiers .snd aux SSK@s et USK@s)   - Courriel (publication via SMTP/mixmaster/mixminion, lecture via
    procmail/etc)   - Usenet (publication via NNTP ou des remailers, lecture via (proxifié)
    NNTP)  - Recherche en texte intégral avec intégration de Lucene  - Extension de HSQLDB pour le chiffrement complet de la base de données  - Heuristiques supplémentaires de gestion des archives

Ce qui sort, et quand, dépend du moment où les choses sont faites.

* 4) Open questions for Syndie

À l'heure actuelle, Syndie a été implémenté avec les primitives cryptographiques standard d'I2P - SHA256, AES256/CBC, ElGamal2048, DSA. Cependant, ce dernier fait figure d'exception, puisqu'il utilise des clés publiques de 1024 bits et repose sur SHA1 (qui s'affaiblit rapidement). Un retour du terrain évoque l'adjonction de SHA256 à DSA, et bien que cela soit réalisable (quoique pas encore standardisé), cela n'offre toutefois que des clés publiques de 1024 bits.

Puisque Syndie n’a pas encore été diffusé publiquement et qu’il n’y a pas de souci de rétrocompatibilité, nous avons le luxe de remplacer les primitives cryptographiques. Une piste consiste à opter pour des signatures ElGamal2048 ou RSA2048 au lieu de DSA, tandis qu’une autre consiste à se tourner vers l’ECC (avec des signatures ECDSA et un chiffrement asymétrique ECIES), peut-être aux niveaux de sécurité 256 bits ou 521 bits (correspondant respectivement à des tailles de clés symétriques de 128 bits et 256 bits).

Quant aux problèmes de brevets concernant l'ECC (cryptographie sur courbes elliptiques), ils ne semblent concerner que certaines optimisations (compression de points) et des algorithmes dont nous n'avons pas besoin (EC MQV). Il n'existe pas grand-chose en termes de prise en charge Java, bien que la bouncycastle lib semble avoir un peu de code. Cependant, il ne serait probablement pas très difficile d'ajouter de petits wrappers à libtomcrypt, openssl ou crypto++ non plus, comme nous l'avons fait pour libGMP (ce qui nous a donné jbigi).

Des avis à ce sujet ?

* 5) ???

Il y a beaucoup à assimiler ci-dessus, c’est pourquoi (sur la suggestion de cervantes) j’envoie ces notes d’état d’avancement si tôt. Si vous avez des commentaires, des questions, des préoccupations ou des suggestions, n’hésitez pas à passer sur #i2p ce soir à 20 h UTC sur irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p pour notre *cough* réunion hebdomadaire !

=jr
