---
title: "Helpers d'adresse authentifiés"
number: "135"
author: "zzz"
created: "2017-02-25"
lastupdated: "2017-02-25"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2241"
---

## Vue d'ensemble

Cette proposition ajoute un mécanisme d'authentification aux URL des helpers d'adresse.

## Motivation

Les URL des helpers d'adresse sont intrinsèquement peu sécurisées. N'importe qui peut inclure un paramètre de helper d'adresse dans un lien, même pour une image, et peut inclure n'importe quelle destination dans le paramètre URL "i2paddresshelper". Selon la mise en œuvre du proxy HTTP de l'utilisateur, cette correspondance nom d'hôte/destination, si elle n'est pas déjà dans le carnet d'adresses, peut être acceptée, soit avec soit sans un intermédiaire pour l'acceptation par l'utilisateur.

## Conception

Les serveurs de saut de confiance et les services d'enregistrement du carnet d'adresses fourniraient de nouveaux liens de helpers d'adresse qui ajoutent des paramètres d'authentification. Les deux nouveaux paramètres seraient une signature en base 64 et une chaîne signée par.

Ces services généreraient et fourniraient un certificat de clé publique. Ce certificat serait disponible pour téléchargement et inclusion dans le logiciel proxy HTTP. Les utilisateurs et les développeurs de logiciels décideraient de faire confiance à ces services en incluant le certificat.

Lorsqu'il rencontre un lien de helper d'adresse, le proxy HTTP vérifie les paramètres d'authentification supplémentaires et tente de vérifier la signature. En cas de vérification réussie, le proxy continuerait comme auparavant, soit en acceptant la nouvelle entrée, soit en affichant un intermédiaire à l'utilisateur. En cas d'échec de la vérification, le proxy pourrait rejeter le helper d'adresse ou afficher des informations supplémentaires à l'utilisateur.

Si aucun paramètre d'authentification n'est présent, le proxy HTTP peut accepter, décliner ou présenter des informations à l'utilisateur.

Les services de saut seraient de confiance comme d'habitude, mais avec l'étape d'authentification supplémentaire. Les liens de helpers d'adresse sur d'autres sites devraient être modifiés.

## Implications en matière de sécurité

Cette proposition ajoute de la sécurité en ajoutant une authentification depuis des services d'enregistrement / de saut de confiance.

## Spécification

À déterminer.

Les deux nouveaux paramètres pourraient être i2paddresshelpersig et i2paddresshelpersigner?

Types de signature acceptés à déterminer. Probablement pas RSA car les signatures en base 64 seraient très longues.

Algorithme de signature : à déterminer. Peut-être simplement hostname=b64dest (comme la proposition 112 pour l'authentification d'enregistrement).

Troisième nouveau paramètre possible : La chaîne d'authentification d'enregistrement (la partie après le "#!") pour être utilisée pour une vérification supplémentaire par le proxy HTTP. Tout "#" dans la chaîne devrait être échappé en "&#35;" ou "&num;", ou être remplacé par un autre caractère sûr pour les URL (à déterminer).

## Migration

Les anciens proxies HTTP qui ne supportent pas les nouveaux paramètres d'authentification les ignoreraient et les transmettraient au serveur web, ce qui devrait être sans danger.

Les nouveaux proxies HTTP qui supportent en option les paramètres d'authentification fonctionneraient bien avec les anciens liens de helpers d'adresse qui ne les contiennent pas.

Les nouveaux proxies HTTP qui exigent des paramètres d'authentification n'autorisaient pas les anciens liens de helpers d'adresse qui ne les contiennent pas.

Les politiques de mise en œuvre d'un proxy peuvent évoluer au cours d'une période de migration.

## Problèmes

Le propriétaire d'un site ne pourrait pas générer un helper d'adresse pour son propre site, car il nécessite la signature d'un serveur de saut de confiance. Il devrait l'enregistrer sur le serveur de confiance et obtenir l'URL du helper authentifié depuis ce serveur. Existe-t-il un moyen pour un site de générer une URL de helper d'adresse auto-authentifié ?

Alternativement, le proxy pourrait vérifier le Referer pour une demande de helper d'adresse. Si le Referer était présent, contenait un b32, et que le b32 correspondait à la destination du helper, alors il pourrait être autorisé comme auto-référencement. Sinon, il pourrait être considéré comme une demande tierce et rejeté.
