---
title: "SAM v2"
description: "Ancien protocole Simple Anonymous Messaging (SAM, protocole d'interface client d'I2P)"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Obsolète :** SAM v2 a été livré avec I2P 0.6.1.31 et n’est plus maintenu. Utilisez [SAM v3](/docs/api/samv3/) pour tout nouveau développement. La seule amélioration de la v2 par rapport à la v1 était la prise en charge de plusieurs sockets multiplexés sur une seule connexion SAM.

## Notes de version

- La chaîne de version indiquée reste `"2.0"`.
- Depuis 0.9.14, le message `HELLO VERSION` accepte des valeurs `MIN`/`MAX` d’un seul chiffre et le paramètre `MIN` est facultatif.
- `DEST GENERATE` prend en charge `SIGNATURE_TYPE`, de sorte que des destinations Ed25519 peuvent être créées.

## Notions de base sur les sessions

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- Chaque destination ne peut avoir qu’une seule session SAM active (flux, datagrammes ou mode brut).
- `STYLE` sélectionne des flux virtuels, des datagrammes signés ou des datagrammes bruts.
- Des options supplémentaires sont transmises à I2CP (par exemple, `tunnels.quantityInbound=3`).
- Les réponses sont identiques à la v1 : `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Encodage des messages

ASCII organisé par lignes, avec des paires `key=value` séparées par des espaces (les valeurs peuvent être entre guillemets). Les types de communication sont les mêmes que dans la v1 :

- Flux via la bibliothèque de streaming I2P
- Datagrammes avec possibilité de réponse (`PROTO_DATAGRAM`)
- Datagrammes bruts (`PROTO_DATAGRAM_RAW`)

## Quand l’utiliser

Uniquement pour les anciens clients qui ne peuvent pas migrer. SAM v3 propose :

- Transfert de destination binaire (`DEST GENERATE BASE64`)
- Sous-sessions et prise en charge de la DHT (table de hachage distribuée) (v3.3)
- Meilleur signalement des erreurs et négociation des options

Reportez-vous à :

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [API des datagrammes](/docs/api/datagrams/)
- [Protocole de diffusion en continu](/docs/specs/streaming/)
