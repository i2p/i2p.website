---
title: "Proposition I2P n° 165 : Correction SSU2"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Ouvert"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

Proposition par weko, orignal, the Anonymous et zzz.

### Aperçu

Ce document suggère des modifications à SSU2 suite à une attaque sur I2P qui a exploitée des vulnérabilités dans SSU2. L'objectif principal est d'améliorer la sécurité et de prévenir les attaques par déni de service distribué (DDoS) et les tentatives de désanonymisation.

### Modèle de menace

Un attaquant crée de nouvelles RIs factices (le routeur n’existe pas) : c’est un RI régulier,
mais il met l'adresse, le port, les clés s et i d'un véritable routeur Bob, puis il
inonde le réseau. Lorsque nous essayons de nous connecter à ce routeur (que nous pensons réel),
nous, en tant qu'Alice, pouvons nous connecter à cette adresse, mais nous ne pouvons pas être
sûr de ce qui a été fait avec le véritable RI de Bob. C'est possible et a été utilisé pour
une attaque par déni de service distribué (créer une grande quantité de ces RIs et inonder
le réseau), cela peut également faciliter les attaques de désanonymisation en impliquant
de bons routeurs tout en épargnant les routeurs de l'attaquant si nous bannissons une IP
avec plusieurs RIs (au lieu de mieux distribuer la construction de tunnel vers ces RIs
comme vers un seul routeur).

### Corrections potentielles

#### 1. Correction avec prise en charge des anciens routeurs (avant la modification)

.. _aperçu-1:

Aperçu
^^^^^^

Une solution de contournement pour prendre en charge les connexions SSU2 avec d'anciens routeurs.

Comportement
^^^^^^^^^^^^

Le profil du routeur de Bob devrait avoir un drapeau 'vérifié', il est faux par défaut
pour tous les nouveaux routeurs (sans profil encore). Lorsque le drapeau 'vérifié' est
faux, nous ne faisons jamais de connexions avec SSU2 comme Alice vers Bob - nous ne pouvons
pas être sûr du RI. Si Bob se connecte à nous (Alice) avec NTCP2 ou SSU2 ou si nous
(Alice) sommes connectés à Bob avec NTCP2 une fois (nous pouvons vérifier le RouterIdent
de Bob dans ces cas) - le drapeau est défini sur vrai.

Problèmes
^^^^^^^^^

Donc, il y a un problème avec l'inondation de faux RI SSU2 seulement : nous ne pouvons pas
le vérifier par nous-mêmes et sommes obligés d'attendre que le véritable routeur établisse
des connexions avec nous.

#### 2. Vérifier RouterIdent lors de la création de connexion

.. _aperçu-2:

Aperçu
^^^^^^

Ajouter un bloc "RouterIdent" pour SessionRequest et SessionCreated.

Format possible du bloc RouterIdent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 octet de drapeaux, 32 octets RouterIdent. Drapeau_0: 0 si RouterIdent du récepteur;
1 si RouterIdent de l'expéditeur.

Comportement
^^^^^^^^^^^^

Alice (devrait(1), peut(2)) envoie dans la charge utile le bloc RouterIdent avec Drapeau_0 = 0
et RouterIdent de Bob. Bob (devrait(3), peut(4)) vérifie si c'est son RouterIdent, et si ce n'est
pas le cas : terminer la session avec raison "RouterIdent incorrect", si c'est son RouterIdent :
envoyer un bloc RI avec 1 dans Drapeau_0 et RouterIdent de Bob.

Avec (1) Bob ne prend pas en charge les anciens routeurs. Avec (2) Bob prend en charge les anciens
routeurs, mais peut être victime d'un DDoS de routeurs qui essaient de se connecter avec de faux RIs.
Avec (3) Alice ne prend pas en charge les anciens routeurs. Avec (4) Alice prend en charge les anciens
routeurs et utilise un schéma hybride : Fix 1 pour les anciens routeurs et Fix 2 pour les nouveaux
routeurs. Si RI indique une nouvelle version, mais que pendant la connexion nous n'avons pas reçu
le bloc RouterIdent - terminer et supprimer le RI.

.. _problèmes-1:

Problèmes
^^^^^^^^^

Un attaquant peut masquer ses faux routeurs comme anciens, et avec (4) nous attendons
pour 'vérifié' comme dans la correction 1 de toute façon.

Remarques
^^^^^^^^^

Au lieu de 32 octets de RouterIdent, nous pouvons probablement utiliser 4 octets siphash-du-hash,
quelque HKDF ou autre chose, ce qui devrait être suffisant.

#### 3. Bob définit i = RouterIdent

.. _aperçu-3:

Aperçu
^^^^^^

Bob utilise son RouterIdent comme clé i.

.. _comportement-1:

Comportement
^^^^^^^^^^^^

Bob (devrait(1), peut(2)) utilise son propre RouterIdent comme clé i pour SSU2.

Alice avec (1) se connecte uniquement si i = RouterIdent de Bob. Alice avec (2) utilise le schéma
hybride (corrections 3 et 1) : si i = RouterIdent de Bob, nous pouvons établir la connexion, sinon
nous devons d'abord la vérifier (voir correction 1).

Avec (1) Alice ne prend pas en charge les anciens routeurs. Avec (2) Alice prend en charge les anciens
routeurs.

.. _problèmes-2:

Problèmes
^^^^^^^^^

Un attaquant peut masquer ses faux routeurs comme anciens, et avec (2) nous attendons
pour 'vérifié' comme dans la correction 1 de toute façon.

.. _remarques-1:

Remarques
^^^^^^^^^

Pour économiser la taille du RI, mieux vaut ajouter une gestion si la clé i n'est pas spécifiée.
Si c'est le cas, alors i = RouterIdent. Dans ce cas, Bob ne prend pas en charge les anciens
routeurs.

#### 4. Ajouter un MixHash supplémentaire au KDF de SessionRequest

.. _aperçu-4:

Aperçu
^^^^^^

Ajouter MixHash(hachage d'identité de Bob) à l'état NOISE du message "SessionRequest", par exemple.
h = SHA256 (h || hachage d'identité de Bob).
Il doit être le dernier MixHash utilisé comme ad pour ENCRYPT ou DECRYPT.
Un drapeau d'en-tête SSU2 supplémentaire "Vérifier l'identité de Bob" = 0x02 doit être introduit.

.. _comportement-4:

Comportement
^^^^^^^^^^^^

- Alice ajoute un MixHash avec le hachage d'identité de Bob à partir du RouterInfo de Bob et l'utilise
comme ad pour ENCRYPT et définit le drapeau "Vérifier l'identité de Bob".
- Bob vérifie le drapeau "Vérifier l'identité de Bob" et ajoute un MixHash avec son propre hachage
d'identité et l'utilise comme ad pour DECRYPT. Si AEAD/Chacha20/Poly1305 échoue, Bob ferme la session.

Compatibilité avec les anciens routeurs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice doit vérifier la version du routeur de Bob et si elle satisfait à la version minimale
prenant en charge cette proposition, ajouter ce MixHash et définir le drapeau "Vérifier l'identité
de Bob". Si le routeur est plus ancien, Alice n'ajoute pas MixHash et ne définit pas le drapeau
"Vérifier l'identité de Bob".
- Bob vérifie le drapeau "Vérifier l'identité de Bob" et ajoute ce MixHash s'il est défini.
Les anciens routeurs ne définissent pas ce drapeau et ce MixHash ne doit pas être ajouté.

.. _problèmes-4:

Problèmes
^^^^^^^^^

- Un attaquant peut prétendre être de faux routeurs avec une version plus ancienne. À un moment donné,
les anciens routeurs doivent être utilisés avec précaution et après avoir été vérifiés par d'autres
moyens.


### Compatibilité ascendante

Décrite dans les corrections.


### Statut actuel

i2pd : Correction 1.
