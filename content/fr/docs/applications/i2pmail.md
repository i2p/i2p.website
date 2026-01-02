---
title: "I2P Mail (courrier électronique anonyme sur I2P)"
description: "Un aperçu des systèmes de messagerie électronique au sein du réseau I2P — historique, options et statut actuel"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Introduction

I2P fournit une messagerie privée de type e-mail via le **service Postman's Mail.i2p** combiné avec **SusiMail**, un client webmail intégré. Ce système permet aux utilisateurs d'envoyer et de recevoir des e-mails à la fois au sein du réseau I2P et vers/depuis l'internet classique (clearnet) via une passerelle.

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** est un fournisseur d'e-mail hébergé à l'intérieur d'I2P, géré par "Postman"
- **SusiMail** est le client webmail intégré dans la console du routeur I2P. Il est conçu pour éviter la fuite de métadonnées (par ex. nom d'hôte) vers les serveurs SMTP externes.
- Grâce à cette configuration, les utilisateurs I2P peuvent envoyer/recevoir des messages à la fois au sein d'I2P et vers/depuis le clearnet (par ex. Gmail) via le pont Postman.

### How Addressing Works

Le courrier électronique I2P utilise un système à double adresse :

- **À l'intérieur du réseau I2P** : `username@mail.i2p` (par ex., `idk@mail.i2p`)
- **Depuis le clearnet** : `username@i2pmail.org` (par ex., `idk@i2pmail.org`)

La passerelle `i2pmail.org` permet aux utilisateurs réguliers d'Internet d'envoyer des emails vers des adresses I2P, et aux utilisateurs I2P d'envoyer vers des adresses clearnet. Les emails Internet sont acheminés via la passerelle avant d'être transférés à travers I2P vers votre boîte de réception SusiMail.

**Quota d'envoi Clearnet** : 20 emails par jour lors de l'envoi vers des adresses internet classiques.

### Ce que c'est

**Pour créer un compte mail.i2p :**

1. Assurez-vous que votre routeur I2P est en cours d'exécution
2. Visitez **[http://hq.postman.i2p](http://hq.postman.i2p)** à l'intérieur d'I2P
3. Suivez le processus d'inscription
4. Accédez à votre courriel via **SusiMail** dans la console du routeur

> **Note** : `hq.postman.i2p` est une adresse réseau I2P (eepsite) et ne peut être accessible que lorsque vous êtes connecté à I2P. Pour plus d'informations sur la configuration, la sécurité et l'utilisation de la messagerie électronique, visitez Postman HQ.

### Comment fonctionne l'adressage

- Suppression automatique des en-têtes identifiants (`User-Agent:`, `X-Mailer:`) pour la confidentialité
- Nettoyage des métadonnées pour éviter les fuites vers les serveurs SMTP externes
- Chiffrement de bout en bout pour les courriels internes I2P-à-I2P

### Démarrage

- Interopérabilité avec l'email "normal" (SMTP/POP) via le pont Postman
- Expérience utilisateur simple (webmail intégré dans la console du routeur)
- Intégré à la distribution I2P de base (SusiMail est fourni avec Java I2P)
- Suppression des en-têtes pour la protection de la vie privée

### Fonctionnalités de confidentialité

- Le pont vers l'email externe nécessite une confiance dans l'infrastructure de Postman
- Le pont vers le clearnet réduit la confidentialité par rapport à une communication purement interne à I2P
- Dépend de la disponibilité et de la sécurité du serveur de messagerie Postman

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

## Technical Details

**Service SMTP** : `localhost:7659` (fourni par Postman) **Service POP3** : `localhost:7660` **Accès Webmail** : Intégré dans la console du routeur à `http://127.0.0.1:7657/susimail/`

> **Important** : SusiMail est uniquement destiné à la lecture et l'envoi d'e-mails. La création et la gestion des comptes doivent être effectuées sur **hq.postman.i2p**.

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte est juste un titre ou semble incomplet, traduisez-le tel quel.

## Best Practices

- **Changez votre mot de passe** après avoir enregistré votre compte mail.i2p
- **Utilisez le courriel I2P-à-I2P** autant que possible pour une confidentialité maximale (pas de passerelle clearnet)
- **Tenez compte de la limite de 20/jour** lors de l'envoi vers des adresses clearnet
- **Comprenez les compromis** : La passerelle clearnet offre la commodité mais réduit l'anonymat comparé aux communications purement internes à I2P
- **Maintenez I2P à jour** pour bénéficier des améliorations de sécurité dans SusiMail

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.
